import datetime
import unittest
import mock
from google.cloud.firestore_v1beta1.proto import firestore_pb2


class TestWatchDocTree(unittest.TestCase):
    def _makeOne(self):
        from google.cloud.firestore_v1beta1.watch import WatchDocTree
        return WatchDocTree()

    def setUp(self):
        self.snapshotted = None

    def test_insert_and_keys(self):
        inst = self._makeOne()
        inst = inst.insert('b', 1)
        inst = inst.insert('a', 2)
        self.assertEqual(sorted(inst.keys()), ['a', 'b'])

    def test_remove_and_keys(self):
        inst = self._makeOne()
        inst = inst.insert('b', 1)
        inst = inst.insert('a', 2)
        inst = inst.remove('a')
        self.assertEqual(sorted(inst.keys()), ['b'])

    def test_insert_and_find(self):
        inst = self._makeOne()
        inst = inst.insert('b', 1)
        inst = inst.insert('a', 2)
        val = inst.find('a')
        self.assertEqual(val.value, 2)

    def test___len__(self):
        inst = self._makeOne()
        inst = inst.insert('b', 1)
        inst = inst.insert('a', 2)
        self.assertEqual(len(inst), 2)


class TestDocumentChange(unittest.TestCase):
    def _makeOne(self, type, document, old_index, new_index):
        from google.cloud.firestore_v1beta1.watch import DocumentChange
        return DocumentChange(type, document, old_index, new_index)

    def test_ctor(self):
        inst = self._makeOne('type', 'document', 'old_index', 'new_index')
        self.assertEqual(inst.type, 'type')
        self.assertEqual(inst.document, 'document')
        self.assertEqual(inst.old_index, 'old_index')
        self.assertEqual(inst.new_index, 'new_index')


class TestWatchResult(unittest.TestCase):
    def _makeOne(self, snapshot, name, change_type):
        from google.cloud.firestore_v1beta1.watch import WatchResult
        return WatchResult(snapshot, name, change_type)

    def test_ctor(self):
        inst = self._makeOne('snapshot', 'name', 'change_type')
        self.assertEqual(inst.snapshot, 'snapshot')
        self.assertEqual(inst.name, 'name')
        self.assertEqual(inst.change_type, 'change_type')


class Test_maybe_wrap_exception(unittest.TestCase):
    def _callFUT(self, exc):
        from google.cloud.firestore_v1beta1.watch import _maybe_wrap_exception
        return _maybe_wrap_exception(exc)

    def test_is_grpc_error(self):
        import grpc
        from google.api_core.exceptions import GoogleAPICallError
        exc = grpc.RpcError()
        result = self._callFUT(exc)
        self.assertEqual(result.__class__, GoogleAPICallError)

    def test_is_not_grpc_error(self):
        exc = ValueError()
        result = self._callFUT(exc)
        self.assertEqual(result.__class__, ValueError)


class Test_document_watch_comparator(unittest.TestCase):
    def _callFUT(self, doc1, doc2):
        from google.cloud.firestore_v1beta1.watch import (
            document_watch_comparator,
            )
        return document_watch_comparator(doc1, doc2)

    def test_same_doc(self):
        result = self._callFUT(1, 1)
        self.assertEqual(result, 0)

    def test_diff_doc(self):
        self.assertRaises(AssertionError, self._callFUT, 1, 2)


class TestWatch(unittest.TestCase):
    def _makeOne(
            self,
            document_reference=None,
            firestore=None,
            target=None,
            comparator=None,
            snapshot_callback=None,
            snapshot_class=None,
            reference_class=None
            ):
        from google.cloud.firestore_v1beta1.watch import Watch
        if document_reference is None:
            document_reference = DummyDocumentReference()
        if firestore is None:
            firestore = DummyFirestore()
        if target is None:
            WATCH_TARGET_ID = 0x5079  # "Py"
            target = {
                'documents': {
                    'documents': ['/']},
                'target_id': WATCH_TARGET_ID
            }
        if comparator is None:
            comparator = self._document_watch_comparator
        if snapshot_callback is None:
            snapshot_callback = self._snapshot_callback
        if snapshot_class is None:
            snapshot_class = DummyDocumentSnapshot
        if reference_class is None:
            reference_class = DummyDocumentReference
        inst = Watch(
            document_reference,
            firestore,
            target,
            comparator,
            snapshot_callback,
            snapshot_class,
            reference_class,
            BackgroundConsumer=DummyBackgroundConsumer,
            ResumableBidiRpc=DummyRpc,
            )
        return inst

    def _document_watch_comparator(self, doc1, doc2):
        return 0

    def _snapshot_callback(self, docs, changes, read_time):
        self.snapshotted = (docs, changes, read_time)

    def test_ctor(self):
        inst = self._makeOne()
        self.assertTrue(inst._consumer.started)
        self.assertTrue(inst.rpc.callbacks, [inst._on_rpc_done])

    def test__on_rpc_done(self):
        inst = self._makeOne()
        threading = DummyThreading()
        with mock.patch(
                'google.cloud.firestore_v1beta1.watch.threading',
                threading
                ):
            inst._on_rpc_done(True)
        from google.cloud.firestore_v1beta1.watch import _RPC_ERROR_THREAD_NAME
        self.assertTrue(threading.threads[_RPC_ERROR_THREAD_NAME].started)

    def test_close(self):
        inst = self._makeOne()
        inst.close()
        self.assertEqual(inst._consumer, None)
        self.assertEqual(inst._rpc, None)
        self.assertTrue(inst._closed)

    def test_close_already_closed(self):
        inst = self._makeOne()
        inst._closed = True
        old_consumer = inst._consumer
        inst.close()
        self.assertEqual(inst._consumer, old_consumer)

    def test_close_inactive(self):
        inst = self._makeOne()
        old_consumer = inst._consumer
        old_consumer.is_active = False
        inst.close()
        self.assertEqual(old_consumer.stopped, False)

    def test_unsubscribe(self):
        inst = self._makeOne()
        inst.unsubscribe()
        self.assertTrue(inst.rpc.closed)

    def test_for_document(self):
        from google.cloud.firestore_v1beta1.watch import Watch
        docref = DummyDocumentReference()
        snapshot_callback = self._snapshot_callback
        snapshot_class_instance = DummyDocumentSnapshot
        document_reference_class_instance = DummyDocumentReference
        modulename = 'google.cloud.firestore_v1beta1.watch'
        with mock.patch(
                '%s.Watch.ResumableBidiRpc' % modulename,
                DummyRpc,
                ):
            with mock.patch(
                    '%s.Watch.BackgroundConsumer' % modulename,
                    DummyBackgroundConsumer,
                    ):
                inst = Watch.for_document(
                    docref,
                    snapshot_callback,
                    snapshot_class_instance,
                    document_reference_class_instance
                )
        self.assertTrue(inst._consumer.started)
        self.assertTrue(inst.rpc.callbacks, [inst._on_rpc_done])

    def test_on_snapshot_target_no_change_no_target_ids_not_current(self):
        inst = self._makeOne()
        proto = DummyProto()
        inst.on_snapshot(proto)  # nothing to assert, no mutations, no rtnval

    def test_on_snapshot_target_no_change_no_target_ids_current(self):
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change.read_time = 1
        inst.current = True

        def push(read_time, next_resume_token):
            inst._read_time = read_time
            inst._next_resume_token = next_resume_token

        inst.push = push
        inst.on_snapshot(proto)
        self.assertEqual(inst._read_time, 1)
        self.assertEqual(inst._next_resume_token, None)

    def test_on_snapshot_target_add(self):
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change.target_change_type = firestore_pb2.TargetChange.ADD
        proto.target_change.target_ids = [1]  # not "Py"
        with self.assertRaises(Exception) as exc:
            inst.on_snapshot(proto)
        self.assertEqual(
            str(exc.exception),
            'Unexpected target ID sent by server'
            )

    def test_on_snapshot_target_remove(self):
        inst = self._makeOne()
        proto = DummyProto()
        target_change = proto.target_change
        target_change.target_change_type = firestore_pb2.TargetChange.REMOVE
        with self.assertRaises(Exception) as exc:
            inst.on_snapshot(proto)
        self.assertEqual(str(exc.exception), 'Error 1:  hi')

    def test_on_snapshot_target_reset(self):
        inst = self._makeOne()

        def reset():
            inst._docs_reset = True

        inst._reset_docs = reset
        proto = DummyProto()
        target_change = proto.target_change
        target_change.target_change_type = firestore_pb2.TargetChange.RESET
        inst.on_snapshot(proto)
        self.assertTrue(inst._docs_reset)

    def test_on_snapshot_target_current(self):
        inst = self._makeOne()
        inst.current = False
        proto = DummyProto()
        target_change = proto.target_change
        target_change.target_change_type = firestore_pb2.TargetChange.CURRENT
        inst.on_snapshot(proto)
        self.assertTrue(inst.current)

    def test_on_snapshot_target_unknown(self):
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change.target_change_type = 'unknown'
        with self.assertRaises(Exception) as exc:
            inst.on_snapshot(proto)
        self.assertTrue(inst._consumer.stopped)
        self.assertEqual(
            str(exc.exception),
            'Unknown target change type: unknown '
        )

    def test_on_snapshot_document_change_removed(self):
        from google.cloud.firestore_v1beta1.watch import (
            WATCH_TARGET_ID,
            ChangeType,
            )
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change = ''
        proto.document_change.removed_target_ids = [WATCH_TARGET_ID]

        class DummyDocument:
            name = 'fred'

        proto.document_change.document = DummyDocument()
        inst.on_snapshot(proto)
        self.assertTrue(inst.change_map['fred'] is ChangeType.REMOVED)

    def test_on_snapshot_document_change_changed(self):
        from google.cloud.firestore_v1beta1.watch import WATCH_TARGET_ID
        inst = self._makeOne()

        def message_to_dict(document):
            return {'fields': None}

        inst.MessageToDict = message_to_dict
        proto = DummyProto()
        proto.target_change = ''
        proto.document_change.target_ids = [WATCH_TARGET_ID]

        class DummyDocument:
            name = 'fred'
            create_time = None
            update_time = None

        proto.document_change.document = DummyDocument()
        inst.on_snapshot(proto)
        self.assertEqual(inst.change_map['fred'].data, None)

    def test_on_snapshot_document_removed(self):
        from google.cloud.firestore_v1beta1.watch import ChangeType
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change = ''
        proto.document_change = ''

        class DummyRemove(object):
            document = 'fred'

        remove = DummyRemove()
        proto.document_remove = remove
        proto.document_delete = None
        inst.on_snapshot(proto)
        self.assertTrue(inst.change_map['fred'] is ChangeType.REMOVED)

    def test_on_snapshot_filter_update(self):
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change = ''
        proto.document_change = ''
        proto.document_remove = None
        proto.document_delete = None

        class DummyFilter(object):
            count = 999

        proto.filter = DummyFilter()

        def reset():
            inst._docs_reset = True

        inst._reset_docs = reset
        inst.on_snapshot(proto)
        self.assertTrue(inst._docs_reset)

    def test_on_snapshot_unknown_listen_type(self):
        inst = self._makeOne()
        proto = DummyProto()
        proto.target_change = ''
        proto.document_change = ''
        proto.document_remove = None
        proto.document_delete = None
        proto.filter = ''
        with self.assertRaises(Exception) as exc:
            inst.on_snapshot(proto)
        self.assertTrue(
            str(exc.exception).startswith('Unknown listen response type'),
            str(exc.exception)
        )

    def test_push_no_changes(self):
        class DummyReadTime(object):
            seconds = 1534858278
        inst = self._makeOne()
        inst.push(DummyReadTime, 'token')
        self.assertEqual(
            self.snapshotted,
            ([], [], datetime.datetime(2018, 8, 21, 6, 31, 18)),
            )
        self.assertTrue(inst.has_pushed)
        self.assertEqual(inst.resume_token, 'token')

    def test__current_size_empty(self):
        inst = self._makeOne()
        result = inst._current_size()
        self.assertEqual(result, 0)

    def test__current_size_docmap_has_one(self):
        inst = self._makeOne()
        inst.doc_map['a'] = 1
        result = inst._current_size()
        self.assertEqual(result, 1)

    def test__affects_target_target_id_None(self):
        inst = self._makeOne()
        self.assertTrue(inst._affects_target(None, []))

    def test__affects_target_current_id_in_target_ids(self):
        inst = self._makeOne()
        self.assertTrue(inst._affects_target([1], 1))

    def test__affects_target_current_id_not_in_target_ids(self):
        inst = self._makeOne()
        self.assertFalse(inst._affects_target([1], 2))

    def test__extract_changes_doc_removed(self):
        from google.cloud.firestore_v1beta1.watch import ChangeType
        inst = self._makeOne()
        changes = {'name': ChangeType.REMOVED}
        doc_map = {'name': True}
        results = inst._extract_changes(doc_map, changes, None)
        self.assertEqual(results, (['name'], [], []))

    def test__extract_changes_doc_updated(self):
        inst = self._makeOne()

        class Dummy(object):
            pass

        doc = Dummy()
        snapshot = Dummy()
        changes = {'name': snapshot}
        doc_map = {'name': doc}
        results = inst._extract_changes(doc_map, changes, 1)
        self.assertEqual(results, ([], [], [snapshot]))
        self.assertEqual(snapshot.read_time, 1)

    def test__extract_changes_doc_added(self):
        inst = self._makeOne()

        class Dummy(object):
            pass

        snapshot = Dummy()
        changes = {'name': snapshot}
        doc_map = {}
        results = inst._extract_changes(doc_map, changes, 1)
        self.assertEqual(results, ([], [snapshot], []))
        self.assertEqual(snapshot.read_time, 1)

    def test__compute_snapshot_doctree_and_docmap_disagree_about_length(self):
        inst = self._makeOne()
        doc_tree = {}
        doc_map = {None: None}
        self.assertRaises(
            AssertionError,
            inst._compute_snapshot, doc_tree, doc_map, None, None, None,
            )

    def test__compute_snapshot_operation_relative_ordering(self):
        from google.cloud.firestore_v1beta1.watch import WatchDocTree
        doc_tree = WatchDocTree()

        class DummyDoc(object):
            update_time = mock.sentinel

        deleted_doc = DummyDoc()
        added_doc = DummyDoc()
        added_doc._document_path = '/added'
        updated_doc = DummyDoc()
        updated_doc._document_path = '/updated'
        doc_tree = doc_tree.insert('/deleted', deleted_doc)
        doc_tree = doc_tree.insert('/updated', updated_doc)
        doc_map = {'/deleted': deleted_doc, '/updated': updated_doc}
        added_snapshot = DummyDocumentSnapshot(added_doc, None, True,
                                               None, None, None)
        added_snapshot.reference = added_doc
        updated_snapshot = DummyDocumentSnapshot(updated_doc, None, True,
                                                 None, None, None)
        updated_snapshot.reference = updated_doc
        delete_changes = ['/deleted']
        add_changes = [added_snapshot]
        update_changes = [updated_snapshot]
        inst = self._makeOne()
        updated_tree, updated_map, applied_changes = inst._compute_snapshot(
            doc_tree,
            doc_map,
            delete_changes,
            add_changes,
            update_changes
            )
        # TODO:
        # Assertion is not verified correct below. Verify this test is good.
        self.assertEqual(updated_map,
                         {
                             '/updated': updated_snapshot,
                             '/added': added_snapshot,
                         })

    def test__reset_docs(self):
        from google.cloud.firestore_v1beta1.watch import ChangeType
        inst = self._makeOne()
        inst.change_map = {None: None}
        from google.cloud.firestore_v1beta1.watch import WatchDocTree
        doc = DummyDocumentReference()
        doc._document_path = '/doc'
        doc_tree = WatchDocTree()
        doc_tree = doc_tree.insert('/doc', doc)
        doc_tree = doc_tree.insert('/doc', doc)
        snapshot = DummyDocumentSnapshot(doc, None, True, None, None, None)
        snapshot.reference = doc
        inst.doc_tree = doc_tree
        inst._reset_docs()
        self.assertEqual(inst.change_map, {'/doc': ChangeType.REMOVED})
        self.assertEqual(inst.resume_token, None)
        self.assertFalse(inst.current)


class DummyFirestoreStub(object):
    def Listen(self):
        pass


class DummyFirestoreClient(object):
    def __init__(self):
        self.firestore_stub = DummyFirestoreStub()


class DummyDocumentReference(object):
    def __init__(self, *document_path, **kw):
        if 'client' not in kw:
            self._client = DummyFirestore()
        else:
            self._client = kw['client']

        self._path = document_path
        self.__dict__.update(kw)

    _document_path = '/'


class DummyFirestore(object):
    _firestore_api = DummyFirestoreClient()
    _database_string = ''

    def document(self, *document_path):
        if len(document_path) == 1:
            path = document_path[0].split('/')
        else:
            path = document_path

        return DummyDocumentReference(*path, client=self)


class DummyDocumentSnapshot(object):
    # def __init__(self, **kw):
    #     self.__dict__.update(kw)
    def __init__(self, reference, data, exists,
                 read_time, create_time, update_time):
        self.reference = reference
        self.data = data
        self.exists = exists
        self.read_time = read_time
        self.create_time = create_time
        self.update_time = update_time


class DummyBackgroundConsumer(object):
    started = False
    stopped = False
    is_active = True

    def __init__(self, rpc, on_snapshot):
        self.rpc = rpc
        self.on_snapshot = on_snapshot

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True
        self.is_active = False


class DummyThread(object):
    started = False

    def __init__(self, name, target, kwargs):
        self.name = name
        self.target = target
        self.kwargs = kwargs

    def start(self):
        self.started = True


class DummyThreading(object):
    def __init__(self):
        self.threads = {}

    def Thread(self, name, target, kwargs):
        thread = DummyThread(name, target, kwargs)
        self.threads[name] = thread
        return thread


class DummyRpc(object):
    def __init__(self, listen, initial_request, should_recover):
        self.listen = listen
        self.initial_request = initial_request
        self.should_recover = should_recover
        self.closed = False
        self.callbacks = []

    def add_done_callback(self, callback):
        self.callbacks.append(callback)

    def close(self):
        self.closed = True


class DummyCause(object):
    code = 1
    message = 'hi'


class DummyChange(object):
    def __init__(self):
        self.target_ids = []
        self.removed_target_ids = []
        self.read_time = 0
        self.target_change_type = firestore_pb2.TargetChange.NO_CHANGE
        self.resume_token = None
        self.cause = DummyCause()


class DummyProto(object):
    def __init__(self):
        self.target_change = DummyChange()
        self.document_change = DummyChange()
