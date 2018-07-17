# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/automl_v1beta1/proto/model_evaluation.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.cloud.automl_v1beta1.proto import translation_pb2 as google_dot_cloud_dot_automl__v1beta1_dot_proto_dot_translation__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/cloud/automl_v1beta1/proto/model_evaluation.proto',
  package='google.cloud.automl.v1beta1',
  syntax='proto3',
  serialized_pb=_b('\n8google/cloud/automl_v1beta1/proto/model_evaluation.proto\x12\x1bgoogle.cloud.automl.v1beta1\x1a\x1cgoogle/api/annotations.proto\x1a\x33google/cloud/automl_v1beta1/proto/translation.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xc8\x02\n\x0fModelEvaluation\x12T\n\x16\x63lassification_metrics\x18\x03 \x01(\x0b\x32\x32.google.cloud.automl.v1beta1.ClassificationMetricsH\x00\x12X\n\x13translation_metrics\x18\x04 \x01(\x0b\x32\x39.google.cloud.automl.v1beta1.TranslationEvaluationMetricsH\x00\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1a\n\x12\x61nnotation_spec_id\x18\x02 \x01(\t\x12/\n\x0b\x63reate_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1f\n\x17\x65valuated_example_count\x18\x06 \x01(\x05\x42\t\n\x07metrics\"\xf5\x04\n\x15\x43lassificationMetrics\x12\x0e\n\x06\x61u_prc\x18\x01 \x01(\x02\x12\x13\n\x0b\x62\x61se_au_prc\x18\x02 \x01(\x02\x12k\n\x18\x63onfidence_metrics_entry\x18\x04 \x03(\x0b\x32I.google.cloud.automl.v1beta1.ClassificationMetrics.ConfidenceMetricsEntry\x12\\\n\x10\x63onfusion_matrix\x18\x05 \x01(\x0b\x32\x42.google.cloud.automl.v1beta1.ClassificationMetrics.ConfusionMatrix\x12\x1a\n\x12\x61nnotation_spec_id\x18\x06 \x03(\t\x1a\xac\x01\n\x16\x43onfidenceMetricsEntry\x12\x1c\n\x14\x63onfidence_threshold\x18\x01 \x01(\x02\x12\x0e\n\x06recall\x18\x02 \x01(\x02\x12\x11\n\tprecision\x18\x03 \x01(\x02\x12\x10\n\x08\x66\x31_score\x18\x04 \x01(\x02\x12\x12\n\nrecall_at1\x18\x05 \x01(\x02\x12\x15\n\rprecision_at1\x18\x06 \x01(\x02\x12\x14\n\x0c\x66\x31_score_at1\x18\x07 \x01(\x02\x1a\xa0\x01\n\x0f\x43onfusionMatrix\x12\x1a\n\x12\x61nnotation_spec_id\x18\x01 \x03(\t\x12S\n\x03row\x18\x02 \x03(\x0b\x32\x46.google.cloud.automl.v1beta1.ClassificationMetrics.ConfusionMatrix.Row\x1a\x1c\n\x03Row\x12\x15\n\rexample_count\x18\x01 \x03(\x05\x42\x66\n\x1f\x63om.google.cloud.automl.v1beta1P\x01ZAgoogle.golang.org/genproto/googleapis/cloud/automl/v1beta1;automlb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_cloud_dot_automl__v1beta1_dot_proto_dot_translation__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_MODELEVALUATION = _descriptor.Descriptor(
  name='ModelEvaluation',
  full_name='google.cloud.automl.v1beta1.ModelEvaluation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='classification_metrics', full_name='google.cloud.automl.v1beta1.ModelEvaluation.classification_metrics', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='translation_metrics', full_name='google.cloud.automl.v1beta1.ModelEvaluation.translation_metrics', index=1,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.cloud.automl.v1beta1.ModelEvaluation.name', index=2,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='annotation_spec_id', full_name='google.cloud.automl.v1beta1.ModelEvaluation.annotation_spec_id', index=3,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_time', full_name='google.cloud.automl.v1beta1.ModelEvaluation.create_time', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='evaluated_example_count', full_name='google.cloud.automl.v1beta1.ModelEvaluation.evaluated_example_count', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='metrics', full_name='google.cloud.automl.v1beta1.ModelEvaluation.metrics',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=206,
  serialized_end=534,
)


_CLASSIFICATIONMETRICS_CONFIDENCEMETRICSENTRY = _descriptor.Descriptor(
  name='ConfidenceMetricsEntry',
  full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfidenceMetricsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='confidence_threshold', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfidenceMetricsEntry.confidence_threshold', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='recall', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfidenceMetricsEntry.recall', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='precision', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfidenceMetricsEntry.precision', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='f1_score', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfidenceMetricsEntry.f1_score', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='recall_at1', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfidenceMetricsEntry.recall_at1', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='precision_at1', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfidenceMetricsEntry.precision_at1', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='f1_score_at1', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfidenceMetricsEntry.f1_score_at1', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=831,
  serialized_end=1003,
)

_CLASSIFICATIONMETRICS_CONFUSIONMATRIX_ROW = _descriptor.Descriptor(
  name='Row',
  full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfusionMatrix.Row',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='example_count', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfusionMatrix.Row.example_count', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1138,
  serialized_end=1166,
)

_CLASSIFICATIONMETRICS_CONFUSIONMATRIX = _descriptor.Descriptor(
  name='ConfusionMatrix',
  full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfusionMatrix',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='annotation_spec_id', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfusionMatrix.annotation_spec_id', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='row', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.ConfusionMatrix.row', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CLASSIFICATIONMETRICS_CONFUSIONMATRIX_ROW, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1006,
  serialized_end=1166,
)

_CLASSIFICATIONMETRICS = _descriptor.Descriptor(
  name='ClassificationMetrics',
  full_name='google.cloud.automl.v1beta1.ClassificationMetrics',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='au_prc', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.au_prc', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='base_au_prc', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.base_au_prc', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='confidence_metrics_entry', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.confidence_metrics_entry', index=2,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='confusion_matrix', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.confusion_matrix', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='annotation_spec_id', full_name='google.cloud.automl.v1beta1.ClassificationMetrics.annotation_spec_id', index=4,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CLASSIFICATIONMETRICS_CONFIDENCEMETRICSENTRY, _CLASSIFICATIONMETRICS_CONFUSIONMATRIX, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=537,
  serialized_end=1166,
)

_MODELEVALUATION.fields_by_name['classification_metrics'].message_type = _CLASSIFICATIONMETRICS
_MODELEVALUATION.fields_by_name['translation_metrics'].message_type = google_dot_cloud_dot_automl__v1beta1_dot_proto_dot_translation__pb2._TRANSLATIONEVALUATIONMETRICS
_MODELEVALUATION.fields_by_name['create_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MODELEVALUATION.oneofs_by_name['metrics'].fields.append(
  _MODELEVALUATION.fields_by_name['classification_metrics'])
_MODELEVALUATION.fields_by_name['classification_metrics'].containing_oneof = _MODELEVALUATION.oneofs_by_name['metrics']
_MODELEVALUATION.oneofs_by_name['metrics'].fields.append(
  _MODELEVALUATION.fields_by_name['translation_metrics'])
_MODELEVALUATION.fields_by_name['translation_metrics'].containing_oneof = _MODELEVALUATION.oneofs_by_name['metrics']
_CLASSIFICATIONMETRICS_CONFIDENCEMETRICSENTRY.containing_type = _CLASSIFICATIONMETRICS
_CLASSIFICATIONMETRICS_CONFUSIONMATRIX_ROW.containing_type = _CLASSIFICATIONMETRICS_CONFUSIONMATRIX
_CLASSIFICATIONMETRICS_CONFUSIONMATRIX.fields_by_name['row'].message_type = _CLASSIFICATIONMETRICS_CONFUSIONMATRIX_ROW
_CLASSIFICATIONMETRICS_CONFUSIONMATRIX.containing_type = _CLASSIFICATIONMETRICS
_CLASSIFICATIONMETRICS.fields_by_name['confidence_metrics_entry'].message_type = _CLASSIFICATIONMETRICS_CONFIDENCEMETRICSENTRY
_CLASSIFICATIONMETRICS.fields_by_name['confusion_matrix'].message_type = _CLASSIFICATIONMETRICS_CONFUSIONMATRIX
DESCRIPTOR.message_types_by_name['ModelEvaluation'] = _MODELEVALUATION
DESCRIPTOR.message_types_by_name['ClassificationMetrics'] = _CLASSIFICATIONMETRICS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ModelEvaluation = _reflection.GeneratedProtocolMessageType('ModelEvaluation', (_message.Message,), dict(
  DESCRIPTOR = _MODELEVALUATION,
  __module__ = 'google.cloud.automl_v1beta1.proto.model_evaluation_pb2'
  ,
  __doc__ = """Evaluation results of a model. (- Next ID: 8 -)
  
  
  Attributes:
      metrics:
          Output only. Problem type specific evaluation metrics.
      classification_metrics:
          Evaluation metrics for models on classification problems.
      translation_metrics:
          Evaluation metrics for models on translation.
      name:
          Output only. Resource name of the model evaluation. Format:  `
          `projects/{project_id}/locations/{location_id}/models/{model_i
          d}/modelEvaluations/{model_evaluation_id}``
      annotation_spec_id:
          Output only. Evaluated annotation spec id. Only non empty if
          the ``ModelEvaluation`` is for a single annotation spec.
      create_time:
          Output only. Timestamp when this model evaluation was created.
      evaluated_example_count:
          The number of examples used for model evaluation.
  """,
  # @@protoc_insertion_point(class_scope:google.cloud.automl.v1beta1.ModelEvaluation)
  ))
_sym_db.RegisterMessage(ModelEvaluation)

ClassificationMetrics = _reflection.GeneratedProtocolMessageType('ClassificationMetrics', (_message.Message,), dict(

  ConfidenceMetricsEntry = _reflection.GeneratedProtocolMessageType('ConfidenceMetricsEntry', (_message.Message,), dict(
    DESCRIPTOR = _CLASSIFICATIONMETRICS_CONFIDENCEMETRICSENTRY,
    __module__ = 'google.cloud.automl_v1beta1.proto.model_evaluation_pb2'
    ,
    __doc__ = """Metrics for a single confidence threshold.
    
    
    Attributes:
        confidence_threshold:
            The confidence threshold value used to compute the metrics.
        recall:
            Recall under the given confidence threshold.
        precision:
            Precision under the given confidence threshold.
        f1_score:
            The harmonic mean of recall and precision.
        recall_at1:
            The recall when only considering the label that has the
            highest prediction score and not below the confidence
            threshold for each example.
        precision_at1:
            The precision when only considering the label that has the
            highest prediction score and not below the confidence
            threshold for each example.
        f1_score_at1:
            The harmonic mean of [recall\_at1][google.cloud.automl.v1beta1
            .ClassificationMetrics.ConfidenceMetricsEntry.recall\_at1] and
            [precision\_at1][google.cloud.automl.v1beta1.ClassificationMet
            rics.ConfidenceMetricsEntry.precision\_at1].
    """,
    # @@protoc_insertion_point(class_scope:google.cloud.automl.v1beta1.ClassificationMetrics.ConfidenceMetricsEntry)
    ))
  ,

  ConfusionMatrix = _reflection.GeneratedProtocolMessageType('ConfusionMatrix', (_message.Message,), dict(

    Row = _reflection.GeneratedProtocolMessageType('Row', (_message.Message,), dict(
      DESCRIPTOR = _CLASSIFICATIONMETRICS_CONFUSIONMATRIX_ROW,
      __module__ = 'google.cloud.automl_v1beta1.proto.model_evaluation_pb2'
      ,
      __doc__ = """A row in the confusion matrix.
      
      
      Attributes:
          example_count:
              Value of the specific cell in the confusion matrix. The number
              of values each row is equal to the size of
              annotatin\_spec\_id.
      """,
      # @@protoc_insertion_point(class_scope:google.cloud.automl.v1beta1.ClassificationMetrics.ConfusionMatrix.Row)
      ))
    ,
    DESCRIPTOR = _CLASSIFICATIONMETRICS_CONFUSIONMATRIX,
    __module__ = 'google.cloud.automl_v1beta1.proto.model_evaluation_pb2'
    ,
    __doc__ = """Confusion matrix of the model running the classification.
    
    
    Attributes:
        annotation_spec_id:
            IDs of the annotation specs used in the confusion matrix.
        row:
            Rows in the confusion matrix. The number of rows is equal to
            the size of ``annotation_spec_id``. ``row[i].value[j]`` is the
            number of examples that have ground truth of the
            ``annotation_spec_id[i]`` and are predicted as
            ``annotation_spec_id[j]`` by the model being evaluated.
    """,
    # @@protoc_insertion_point(class_scope:google.cloud.automl.v1beta1.ClassificationMetrics.ConfusionMatrix)
    ))
  ,
  DESCRIPTOR = _CLASSIFICATIONMETRICS,
  __module__ = 'google.cloud.automl_v1beta1.proto.model_evaluation_pb2'
  ,
  __doc__ = """Model evaluation metrics for classification problems.
  
  
  Attributes:
      au_prc:
          The Area under precision recall curve metric.
      base_au_prc:
          The Area under precision recall curve metric based on priors.
      confidence_metrics_entry:
          Metrics that have confidence thresholds. Precision-recall
          curve can be derived from it.
      confusion_matrix:
          Confusion matrix of the evaluation. Only set for MULTICLASS
          classification problems where number of labels is no more than
          10. Only set for model level evaluation, not for evaluation
          per label.
      annotation_spec_id:
          The annotation spec ids used for this evaluation.
  """,
  # @@protoc_insertion_point(class_scope:google.cloud.automl.v1beta1.ClassificationMetrics)
  ))
_sym_db.RegisterMessage(ClassificationMetrics)
_sym_db.RegisterMessage(ClassificationMetrics.ConfidenceMetricsEntry)
_sym_db.RegisterMessage(ClassificationMetrics.ConfusionMatrix)
_sym_db.RegisterMessage(ClassificationMetrics.ConfusionMatrix.Row)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\037com.google.cloud.automl.v1beta1P\001ZAgoogle.golang.org/genproto/googleapis/cloud/automl/v1beta1;automl'))
# @@protoc_insertion_point(module_scope)
