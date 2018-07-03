# Copyright 2017, Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Bi-directional streaming RPC helpers."""

import logging
import threading

from six.moves import queue

from google.api_core import exceptions

_LOGGER = logging.getLogger(__name__)
_BIDIRECTIONAL_CONSUMER_NAME = 'Thread-ConsumeBidirectionalStream'


class _RequestQueueGenerator(object):
    """A helper for sending requests to a gRPC stream from a Queue.

    This generator takes requests off a given queue and yields them to gRPC.

    This helper is useful when you have an indeterminate, indefinite, or
    otherwise open-ended set of requests to send through a request-streaming
    (or bidirectional) RPC.

    The reason this is necessary is because gRPC takes an iterator as the
    request for request-streaming RPCs. gRPC consumes this iterator in another
    thread to allow it to block while generating requests for the stream.
    However, if the generator blocks indefinitely gRPC will not be able to
    clean up the thread as it'll be blocked on `next(iterator)` and not be able
    to check the channel status to stop iterating. This helper mitigates that
    by waiting on the queue with a timeout and checking the RPC state before
    yielding.

    Finally, it allows for retrying without swapping queues because if it does
    pull an item off the queue when the RPC is inactive, it'll immediately put
    it back and then exit. This is necessary because yielding the item in this
    case will cause gRPC to discard it. In practice, this means that the order
    of messages is not guaranteed. If such a thing is necessary it would be
    easy to use a priority queue.

    Example::

        requests = request_queue_generator(q)
        call = stub.StreamingRequest(iter(requests))
        requests.call = call

        for response in call:
            print(response)
            q.put(...)

    Note that it is possible to accomplish this behavior without "spinning"
    (using a queue timeout). One possible way would be to use more threads to
    multiplex the grpc end event with the queue, another possible way is to
    use selectors and a custom event/queue object. Both of these approaches
    are significant from an engineering perspective for small benefit - the
    CPU consumed by spinning is pretty minuscule.

    Args:
        queue (queue.Queue): The request queue.
        period (float): The number of seconds to wait for items from the queue
            before checking if the RPC is cancelled. In practice, this
            determines the maximum amount of time the request consumption
            thread will live after the RPC is cancelled.
        initial_request (Union[protobuf.Message,
                Callable[None, protobuf.Message]]): The initial request to
            yield. This is done independently of the request queue to allow fo
            easily restarting streams that require some initial configuration
            request.
    """
    def __init__(self, queue, period=1, initial_request=None):
        self._queue = queue
        self._period = period
        self._initial_request = initial_request
        self.call = None

    def _is_active(self):
        # Note: there is a possibility that this starts *before* the call
        # property is set. So we have to check if self.call is set before
        # seeing if it's active.
        if self.call is not None and not self.call.is_active():
            return False
        else:
            return True

    def __iter__(self):
        if self._initial_request is not None:
            if callable(self._initial_request):
                yield self._initial_request()
            else:
                yield self._initial_request

        while True:
            try:
                item = self._queue.get(timeout=self._period)
            except queue.Empty:
                if not self._is_active():
                    _LOGGER.debug(
                        'Empty queue and inactive call, exiting request '
                        'generator.')
                    return
                else:
                    # call is still active, keep waiting for queue items.
                    continue

            # The consumer explicitly sent "None", indicating that the request
            # should end.
            if item is None:
                _LOGGER.debug('Cleanly exiting request generator.')
                return

            if not self._is_active():
                # We have an item, but the call is closed. We should put the
                # item back on the queue so that the next call can consume it.
                self._queue.put(item)
                _LOGGER.debug(
                    'Inactive call, replacing item on queue and exiting '
                    'request generator.')
                return

            yield item


class BidiRpc(object):
    """A helper for consuming a bi-directional streaming RPC.

    This maps gRPC's built-in interface which uses a request iterator and a
    response iterator into a socket-like :func:`send` and :func:`recv`. This
    is a more useful pattern for long-running or asymmetric streams (streams
    where there is not a direct correlation between the requests and
    responses).

    Example::

        initial_request = example_pb2.StreamingRpcRequest(
            setting='example')
        rpc = BidiRpc(stub.StreamingRpc, initial_request=initial_request)

        rpc.open()

        while rpc.is_active():
            print(rpc.recv())
            rpc.send(example_pb2.StreamingRpcRequest(
                data='example'))

    This does *not* retry the stream on errors. See :class:`ResumableBidiRpc`.

    Args:
        start_rpc (grpc.StreamStreamMultiCallable): The gRPC method used to
            start the RPC.
        initial_request (Union[protobuf.Message,
                Callable[None, protobuf.Message]]): The initial request to
            yield. This is useful if an initial request is needed to start the
            stream.
    """
    def __init__(self, start_rpc, initial_request=None):
        self._start_rpc = start_rpc
        self._initial_request = initial_request
        self._request_queue = queue.Queue()
        self._request_generator = None
        self._is_active = False
        self._callbacks = []
        self.call = None

    def add_done_callback(self, callback):
        """Adds a callback that will be called when the RPC terminates.

        This occurs when the RPC errors or is successfully terminated.

        Args:
            callback (Callable[[grpc.Future], None]): The callback to execute.
                It will be provided with the same gRPC future as the underlying
                stream which will also be a :class:`grpc.Call`.
        """
        self._callbacks.append(callback)

    def _on_call_done(self, future):
        for callback in self._callbacks:
            callback(future)

    def open(self):
        """Opens the stream."""
        if self.is_active:
            raise ValueError('Can not open an already open stream.')

        request_generator = _RequestQueueGenerator(
            self._request_queue, initial_request=self._initial_request)
        print('request generator created')
        call = self._start_rpc(iter(request_generator))

        request_generator.call = call

        # TODO: api_core should expose the future interface for wrapped
        # callables as well.
        if hasattr(call, '_wrapped'):  # pragma: NO COVER
            call._wrapped.add_done_callback(self._on_call_done)
        else:
            call.add_done_callback(self._on_call_done)

        self._request_generator = request_generator
        self.call = call

    def close(self):
        """Closes the stream."""
        if self.call is None:
            return

        self._request_queue.put(None)
        self.call.cancel()
        self._request_generator = None
        # Don't set self.call to None. Keep it around so that send/recv can
        # raise the error.

    def send(self, request):
        """Queue a message to be sent on the stream.

        Send is non-blocking.

        If the underlying RPC has been closed, this will raise.

        Args:
            request (protobuf.Message): The request to send.
        """
        if self.call is None:
            raise ValueError(
                'Can not send() on an RPC that has never been open()ed.')

        # Don't use self.is_active(), as ResumableBidiRpc will overload it
        # to mean something semantically different.
        if self.call.is_active():
            self._request_queue.put(request)
        else:
            # calling next should cause the call to raise.
            next(self.call)

    def recv(self):
        """Wait for a message to be returned from the stream.

        Recv is blocking.

        If the underlying RPC has been closed, this will raise.

        Returns:
            protobuf.Message: The received message.
        """
        if self.call is None:
            raise ValueError(
                'Can not recv() on an RPC that has never been open()ed.')

        return next(self.call)

    @property
    def is_active(self):
        """bool: True if this stream is currently open and active."""
        return self.call is not None and self.call.is_active()

    @property
    def pending_requests(self):
        """int: Returns an estimate of the number of queued requests."""
        return self._request_queue.qsize()


class ResumableBidiRpc(BidiRpc):
    """A :class:`BidiRpc` that can automatically resume the stream on errors.

    It uses the ``should_recover`` arg to determine if it should re-establish
    the stream on error.

    Example::

        def should_recover(exc):
            return (
                isinstance(exc, grpc.RpcError) and
                exc.code() == grpc.StatusCode.UNVAILABLE)

        initial_request = example_pb2.StreamingRpcRequest(
            setting='example')

        rpc = ResumeableBidiRpc(
            stub.StreamingRpc,
            initial_request=initial_request,
            should_recover=should_recover)

        rpc.open()

        while rpc.is_active():
            print(rpc.recv())
            rpc.send(example_pb2.StreamingRpcRequest(
                data='example'))

    Args:
        start_rpc (grpc.StreamStreamMultiCallable): The gRPC method used to
            start the RPC.
        initial_request (Union[protobuf.Message,
                Callable[None, protobuf.Message]]): The initial request to
            yield. This is useful if an initial request is needed to start the
            stream.
        should_recover (Callable[[Exception], bool]): A function that returns
            True if the stream should be recovered. This will be called
            whenever an error is encountered on the stream.
    """
    def __init__(self, start_rpc, should_recover, initial_request=None):
        super(ResumableBidiRpc, self).__init__(start_rpc, initial_request)
        self._should_recover = should_recover
        self._operational_lock = threading.RLock()
        self._finalized = False
        self._finalize_lock = threading.Lock()

    def _finalize(self, result):
        with self._finalize_lock:
            if self._finalized:
                return

            for callback in self._callbacks:
                callback(result)

            self._finalized = True

    def _on_call_done(self, future):
        # Unlike the base class, we only execute the callbacks on a terminal
        # error, not for errors that we can recover from. Note that grpc's
        # "future" here is also a grpc.RpcError.
        if not self._should_recover(future):
            self._finalize(future)
        else:
            _LOGGER.debug('Re-opening stream from gRPC callback.')
            self._reopen()

    def _reopen(self):
        with self._operational_lock:
            # Another thread already managed to re-open this stream.
            if self.call is not None and self.call.is_active():
                _LOGGER.debug('Stream was already re-established.')
                return

            self.call = None
            # Request generator should exit cleanly since the RPC its bound to
            # has exited.
            self.request_generator = None

            # Note: we do not currently do any sort of backoff here. The
            # assumption is that re-establishing the stream under normal
            # circumstances will happen in intervals greater than 60s.
            # However, it is possible in a degenerative case that the server
            # closes the stream rapidly which would lead to thrashing here,
            # but hopefully in those cases the server would return a non-
            # retryable error.

            try:
                self.open()
            # If re-opening or re-calling the method fails for any reason,
            # consider it a terminal error and finalize the stream.
            except Exception as exc:
                self._finalize(exc)
                raise

            _LOGGER.info('Re-established stream')

    def _recoverable(self, method, *args, **kwargs):
        """Wraps a method to recover the stream and retry on error.

        If a retryable error occurs while making the call, then the stream will
        be re-opened and the method will be retried. This happens indefinitely
        so long as the error is a retryable one. If an error occurs while
        re-opening the stream, then this method will raise immediately and
        trigger finalization of this object.

        Args:
            method (Callable[..., Any]): The method to call.
            args: The args to pass to the method.
            kwargs: The kwargs to pass to the method.
        """
        while True:
            try:
                return method(*args, **kwargs)

            except Exception as exc:
                _LOGGER.debug('Call to retryable %r caused %s.', method, exc)
                if not self._should_recover(exc):
                    self.close()
                    _LOGGER.debug('Not retrying %r due to %s.', method, exc)
                    self._finalize(exc)
                    raise exc

            _LOGGER.debug('Re-opening stream from retryable %r.', method)
            self._reopen()

    def send(self, request):
        return self._recoverable(
            super(ResumableBidiRpc, self).send, request)

    def recv(self):
        return self._recoverable(
            super(ResumableBidiRpc, self).recv)

    @property
    def is_active(self):
        """bool: True if this stream is currently open and active."""
        # Use the operational lock. It's entirely possible for something
        # to check the active state *while* the RPC is being retried.
        # Also, use finalized to track the actual terminal state here.
        # This is because if the stream is re-established by the gRPC thread
        # it's technically possible to check this between when gRPC marks the
        # RPC as inactive and when gRPC executes our callback that re-opens
        # the stream.
        with self._operational_lock:
            return self.call is not None and not self._finalized


class BackgroundConsumer(object):
    """A bi-directional stream consumer that runs in a separate thread.

    This maps the consumption of a stream into a callback-based model. It also
    provides :func:`pause` and :func:`resume` to allow for flow-control.

    Example::

        def should_recover(exc):
            return (
                isinstance(exc, grpc.RpcError) and
                exc.code() == grpc.StatusCode.UNVAILABLE)

        initial_request = example_pb2.StreamingRpcRequest(
            setting='example')

        rpc = ResumeableBidiRpc(
            stub.StreamingRpc,
            initial_request=initial_request,
            should_recover=should_recover)

        def on_response(response):
            print(response)

        consumer = BackgroundConsumer(rpc, on_response)
        consumer.start()

    Note that error handling *must* be done by using the provided
    ``bidi_rpc``'s ``add_done_callback``. This helper will automatically exit
    whenever the RPC itself exits and will not provide any error details.

    Args:
        bidi_rpc (BidiRpc): The RPC to consume. Should not have been
            ``open()``ed yet.
        on_response (Callable[[protobuf.Message], None]): The callback to
            be called for every response on the stream.
    """
    def __init__(self, bidi_rpc, on_response):
        self._bidi_rpc = bidi_rpc
        self._on_response = on_response
        self._paused = False
        self._wake = threading.Condition()
        self._thread = None
        self._operational_lock = threading.Lock()

    def _on_call_done(self, future):
        # Resume the thread if it's paused, this prevents blocking forever
        # when the RPC has terminated.
        self.resume()

    def _thread_main(self):
        try:
            self._bidi_rpc.add_done_callback(self._on_call_done)
            self._bidi_rpc.open()

            while self._bidi_rpc.is_active:
                # Do not allow the paused status to change at all during this
                # section. There is a condition where we could be resumed
                # between checking if we are paused and calling wake.wait(),
                # which means that we will miss the notification to wake up
                # (oops!) and wait for a notification that will never come.
                # Keeping the lock throughout avoids that.
                # In the future, we could use `Condition.wait_for` if we drop
                # Python 2.7.
                with self._wake:
                    if self._paused:
                        _LOGGER.debug('paused, waiting for waking.')
                        self._wake.wait()
                        _LOGGER.debug('woken.')

                _LOGGER.debug('waiting for recv.')
                response = self._bidi_rpc.recv()
                _LOGGER.debug('recved response.')
                self._on_response(response)

        except exceptions.GoogleAPICallError as exc:
            _LOGGER.debug(
                '%s caught error %s and will exit. Generally this is due to '
                'the RPC itself being cancelled and the error will be '
                'surfaced to the calling code.',
                _BIDIRECTIONAL_CONSUMER_NAME, exc, exc_info=True)

        except Exception as exc:
            _LOGGER.exception(
                '%s caught unexpected exception %s and will exit.',
                _BIDIRECTIONAL_CONSUMER_NAME, exc)

        else:
            _LOGGER.error(
                'The bidirectional RPC unexpectedly exited. This is a truly '
                'exceptional case. Please file a bug with your logs.')

        _LOGGER.info('%s exiting', _BIDIRECTIONAL_CONSUMER_NAME)

    def start(self):
        """Start the background thread and begin consuming the thread."""
        with self._operational_lock:
            thread = threading.Thread(
                name=_BIDIRECTIONAL_CONSUMER_NAME,
                target=self._thread_main)
            thread.daemon = True
            thread.start()
            self._thread = thread
            _LOGGER.debug('Started helper thread %s', thread.name)

    def stop(self):
        """Stop consuming the stream and shutdown the background thread."""
        with self._operational_lock:
            self._bidi_rpc.close()

            if self._thread is not None:
                # Resume the thread to wake it up in case it is sleeping.
                self.resume()
                self._thread.join()

            self._thread = None

    @property
    def is_active(self):
        """bool: True if the background thread is active."""
        return self._thread is not None and self._thread.is_alive()

    def pause(self):
        """Pauses the response stream.

        This does *not* pause the request stream.
        """
        with self._wake:
            self._paused = True

    def resume(self):
        """Resumes the response stream."""
        with self._wake:
            self._paused = False
            self._wake.notifyAll()

    @property
    def is_paused(self):
        """bool: True if the response stream is paused."""
        return self._paused
