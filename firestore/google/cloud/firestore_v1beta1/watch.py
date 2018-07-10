# Copyright 2017 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import threading
from enum import Enum

from google.cloud.firestore_v1beta1.bidi import ResumableBidiRpc
from google.cloud.firestore_v1beta1.bidi import BackgroundConsumer
from google.cloud.firestore_v1beta1.proto import firestore_pb2
from google.api_core import exceptions
from google.protobuf import json_format


# from bidi import BidiRpc, ResumableBidiRpc
import time
import random
import grpc

"""Python client for Google Cloud Firestore Watch."""

_LOGGER = logging.getLogger(__name__)

WATCH_TARGET_ID = 0x5079  # "Py"

GRPC_STATUS_CODE = {
    'OK': 0,
    'CANCELLED': 1,
    'UNKNOWN': 2,
    'INVALID_ARGUMENT': 3,
    'DEADLINE_EXCEEDED': 4,
    'NOT_FOUND': 5,
    'ALREADY_EXISTS': 6,
    'PERMISSION_DENIED': 7,
    'UNAUTHENTICATED': 16,
    'RESOURCE_EXHAUSTED': 8,
    'FAILED_PRECONDITION': 9,
    'ABORTED': 10,
    'OUT_OF_RANGE': 11,
    'UNIMPLEMENTED': 12,
    'INTERNAL': 13,
    'UNAVAILABLE': 14,
    'DATA_LOSS': 15,
    'DO_NOT_USE': -1
}
_RPC_ERROR_THREAD_NAME = 'Thread-OnRpcTerminated'
_RETRYABLE_STREAM_ERRORS = (
    exceptions.DeadlineExceeded,
    exceptions.ServiceUnavailable,
    exceptions.InternalServerError,
    exceptions.Unknown,
    exceptions.GatewayTimeout
)


def _maybe_wrap_exception(exception):
    """Wraps a gRPC exception class, if needed."""
    if isinstance(exception, grpc.RpcError):
        return exceptions.from_grpc_error(exception)
    return exception


def is_permanent_error(self, error):
    try:
        if (error.code == GRPC_STATUS_CODE['CANCELLED'] or
                error.code == GRPC_STATUS_CODE['UNKNOWN'] or
                error.code == GRPC_STATUS_CODE['DEADLINE_EXCEEDED'] or
                error.code == GRPC_STATUS_CODE['RESOURCE_EXHAUSTED'] or
                error.code == GRPC_STATUS_CODE['INTERNAL'] or
                error.code == GRPC_STATUS_CODE['UNAVAILABLE'] or
                error.code == GRPC_STATUS_CODE['UNAUTHENTICATED']):
            return False
        else:
            return True
    except AttributeError:
        _LOGGER.error("Unable to determine error code")
        return False


def document_watch_comparator(doc1, doc2):
    assert doc1 == doc2, 'Document watches only support one document.'
    return 0


class ExponentialBackOff(object):
    _INITIAL_SLEEP = 1.0
    """float: Initial "max" for sleep interval."""
    _MAX_SLEEP = 30.0
    """float: Eventual "max" sleep time."""
    _MULTIPLIER = 2.0
    """float: Multiplier for exponential backoff."""

    def __init__(self, initial_sleep=_INITIAL_SLEEP, max_sleep=_MAX_SLEEP,
                 multiplier=_MULTIPLIER):
        self.initial_sleep = self.current_sleep = initial_sleep
        self.max_sleep = max_sleep
        self.multipler = multiplier

    def back_off(self):
        self.current_sleep = self._sleep(self.current_sleep,
                                         self.max_sleep,
                                         self.multipler)

    def reset_to_max(self):
        self.current_sleep = self.max_sleep

    def reset(self):
        self.current_sleep = self._INITIAL_SLEEP

    def _sleep(self, current_sleep, max_sleep=_MAX_SLEEP,
               multiplier=_MULTIPLIER):
        """Sleep and produce a new sleep time.

        .. _Exponential Backoff And Jitter: https://www.awsarchitectureblog.com/\
                                            2015/03/backoff.html

        Select a duration between zero and ``current_sleep``. It might seem
        counterintuitive to have so much jitter, but
        `Exponential Backoff And Jitter`_ argues that "full jitter" is
        the best strategy.

        Args:
            current_sleep (float): The current "max" for sleep interval.
            max_sleep (Optional[float]): Eventual "max" sleep time
            multiplier (Optional[float]): Multiplier for exponential backoff.

        Returns:
            float: Newly doubled ``current_sleep`` or ``max_sleep`` (whichever
            is smaller)
        """
        actual_sleep = random.uniform(0.0, self.current_sleep)
        time.sleep(actual_sleep)
        return min(self.multiplier * self.current_sleep, self.max_sleep)


class WatchChangeType(Enum):
    ADDED = 0
    MODIFIED = 1
    REMOVED = 2


class WatchResult(object):
    def __init__(self, snapshot, name, change_type):
        self.snapshot = snapshot
        self.name = name
        self.change_type = change_type


class Watch(object):
    def __init__(self,
                 document_reference,
                 firestore,
                 target,
                 comparator,
                 on_snapshot,
                 DocumentSnapshotCls):
        """
        Args:
            firestore:
            target:
            comparator:
            on_snapshot: Callback method that receives two arguments,
                            list(snapshots) and
                            list(tuple(document_id, change_type))
            DocumentSnapshotCls: instance of the DocumentSnapshot class
        """
        self._document_reference = document_reference
        self._firestore = firestore
        self._api = firestore._firestore_api
        self._targets = target
        self._comparator = comparator
        self._backoff = ExponentialBackOff()
        self.DocumentSnapshot = DocumentSnapshotCls

        def should_recover(exc):
            return (
                isinstance(exc, grpc.RpcError) and
                exc.code() == grpc.StatusCode.UNVAILABLE)

        initial_request = firestore_pb2.ListenRequest(
            database=self._firestore._database_string,
            add_target=self._targets
        )

        self.rpc = ResumableBidiRpc(
            self._api.firestore_stub.Listen,
            initial_request=initial_request,
            should_recover=should_recover)

        self.rpc.add_done_callback(self._on_rpc_done)

        def consumer_callback(response):
            processed_response = self.process_response(response)
            if processed_response:
                _LOGGER.debug("running provided callback")
                on_snapshot(processed_response)

        self._consumer = BackgroundConsumer(self.rpc, consumer_callback)
        self._consumer.start()

    def _on_rpc_done(self, future):
        """Triggered whenever the underlying RPC terminates without recovery.

        This is typically triggered from one of two threads: the background
        consumer thread (when calling ``recv()`` produces a non-recoverable
        error) or the grpc management thread (when cancelling the RPC).

        This method is *non-blocking*. It will start another thread to deal
        with shutting everything down. This is to prevent blocking in the
        background consumer and preventing it from being ``joined()``.
        """
        # TODO: look at pushing this down into the background consumer
        _LOGGER.info(
            'RPC termination has signaled shutdown.')
        future = _maybe_wrap_exception(future)
        thread = threading.Thread(
            name=_RPC_ERROR_THREAD_NAME,
            target=self.close,
            kwargs={'reason': future})
        thread.daemon = True
        thread.start()

    @classmethod
    def for_document(cls, document_ref, on_snapshot, snapshot_class_instance):
        """
        Creates a watch snapshot listener for a document. on_snapshot receives
        a DocumentChange object, but may also start to get targetChange and such
        soon

        Args:
            document_ref: Reference to Document
            on_snapshot: callback to be called on snapshot
            snapshot_class_instance: instance of snapshot cls to make snapshots with to 
                pass to on_snapshot

        """
        return cls(document_ref,
                   document_ref._client,
                   {
                       'documents': {
                           'documents': [document_ref._document_path]},
                       'target_id': WATCH_TARGET_ID
                   },
                   document_watch_comparator,
                   on_snapshot,
                   snapshot_class_instance)

    # @classmethod
    # def for_query(cls, query, on_snapshot):
    #     return cls(query._client,
    #                {
    #                    'query': query.to_proto(),
    #                    'target_id': WATCH_TARGET_ID
    #                },
    #                query.comparator(),
    #                on_snapshot)

    def process_response(self, proto):
        """
        Args:
            listen_response(`google.cloud.firestore_v1beta1.types.ListenResponse`):
                Callback method that receives a object to
        """
        TargetChange = firestore_pb2.TargetChange

        if str(proto.target_change):
            _LOGGER.debug('process_response: Processing target change')

            change = proto.target_change  # google.cloud.firestore_v1beta1.types.TargetChange

            notarget_ids = change.target_ids is None or len(change.target_ids)
            if change.target_change_type == TargetChange.NO_CHANGE:
                _LOGGER.debug("process_response: target change: NO_CHANGE")
                if notarget_ids and change.read_time: # and current:  # current is used to reflect if the local copy of tree is accurate?
                    # This means everything is up-to-date, so emit the current set of
                    # docs as a snapshot, if there were changes.
                    #   push(
                    #     DocumentSnapshot.toISOTime(change.readTime),
                    #     change.resumeToken
                    #   );
                    # }
                    # For now, we can do nothing here since there isn't anything to do
                    # eventually it seems it makes sens to record this as a snapshot?
                    # TODO : node calls the callback with no change?
                    pass
            elif change.target_change_type == TargetChange.ADD:
                _LOGGER.debug("process_response: target change: ADD")
                assert WATCH_TARGET_ID == change.target_ids[0], 'Unexpected target ID sent by server'
                # TODO : do anything here?

                return WatchResult(
                    None,
                    self._document_reference.id,
                    WatchChangeType.ADDED)
            elif change.target_change_type == TargetChange.REMOVE:
                _LOGGER.debug("process_response: target change: REMOVE")

                code = 13
                message = 'internal error'
                if change.cause:
                    code = change.cause.code
                    message = change.cause.message

                # TODO: Surface a .code property on the exception.
                raise Exception('Error ' + code + ': ' + message)
            elif change.target_change_type == TargetChange.RESET:
                _LOGGER.debug("process_response: target change: RESET")

                # // Whatever changes have happened so far no longer matter.
                # resetDocs(); # TODO
                # TODO : do something here?
            elif change.target_change_type == TargetChange.CURRENT:
                _LOGGER.debug("process_response: target change: CURRENT")

                # current = True # TODO
                # TODO: do something here?
            else:
                _LOGGER.info('process_response: Unknown target change ' +
                             str(change.target_change_type))

                # closeStream(
                #   new Error('Unknown target change type: ' + JSON.stringify(change))
                # TODO : make this exit the inner function and stop processing?
                raise Exception('Unknown target change type: ' + str(change))

            if change.resume_token and self._affects_target(change.target_ids,
                                                            WATCH_TARGET_ID):
                self._backoff.reset()

        elif str(proto.document_change):
            _LOGGER.debug('process_response: Processing document change')

            # No other target_ids can show up here, but we still need to see if the
            # targetId was in the added list or removed list.
            target_ids = proto.document_change.target_ids or []
            removed_target_ids = proto.document_change.removed_target_ids or []
            changed = False
            removed = False

            for target in target_ids:
                if target == WATCH_TARGET_ID:
                    changed = True

            for target in removed_target_ids:
                if target == WATCH_TARGET_ID:
                    removed = True

            if changed:
                _LOGGER.debug('Received document change')

                # google.cloud.firestore_v1beta1.types.DocumentChange
                document_change = proto.document_change
                # google.cloud.firestore_v1beta1.types.Document
                document = document_change.document

                data = json_format.MessageToDict(document)

                snapshot = self.DocumentSnapshot(
                    reference=self._document_reference,
                    data=data['fields'],
                    exists=True,
                    read_time=None,
                    create_time=document.create_time,
                    update_time=document.update_time)

                return WatchResult(snapshot,
                                   self._document_reference.id,
                                   WatchChangeType.MODIFIED)

            elif removed:
                _LOGGER.debug('Watch.onSnapshot Received document remove')
                # changeMap.set(name, REMOVED);

        # Document Delete or Document Remove?
        elif (proto.document_delete or proto.document_remove):
            _LOGGER.debug('Watch.onSnapshot Processing remove event')
            #   const name = (proto.document_delete || proto.document_remove).document
            #   changeMap.set(name, REMOVED);
            return WatchResult(None,
                               self._document_reference.id,
                               WatchChangeType.REMOVED)
        elif (proto.filter):
            _LOGGER.debug('Watch.onSnapshot Processing filter update')
            #   if (proto.filter.count !== currentSize()) {
            #     // We need to remove all the current results.
            #     resetDocs();
            #     // The filter didn't match, so re-issue the query.
            #     resetStream();

        else:
            _LOGGER.debug("UNKNOWN TYPE. UHOH")
        #   closeStream(
        #     new Error('Unknown listen response type: ' + JSON.stringify(proto))
        #   )

    def _affects_target(self, target_ids, current_id):
        if target_ids is None or len(target_ids) == 0:
            return True

        for target_id in target_ids:
            if target_id == current_id:
                return True

        return False
