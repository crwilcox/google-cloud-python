# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/automl_v1beta1/proto/prediction_service.proto

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
from google.cloud.automl_v1beta1.proto import annotation_payload_pb2 as google_dot_cloud_dot_automl__v1beta1_dot_proto_dot_annotation__payload__pb2
from google.cloud.automl_v1beta1.proto import data_items_pb2 as google_dot_cloud_dot_automl__v1beta1_dot_proto_dot_data__items__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/cloud/automl_v1beta1/proto/prediction_service.proto',
  package='google.cloud.automl.v1beta1',
  syntax='proto3',
  serialized_pb=_b('\n:google/cloud/automl_v1beta1/proto/prediction_service.proto\x12\x1bgoogle.cloud.automl.v1beta1\x1a\x1cgoogle/api/annotations.proto\x1a:google/cloud/automl_v1beta1/proto/annotation_payload.proto\x1a\x32google/cloud/automl_v1beta1/proto/data_items.proto\"\xd4\x01\n\x0ePredictRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12<\n\x07payload\x18\x02 \x01(\x0b\x32+.google.cloud.automl.v1beta1.ExamplePayload\x12G\n\x06params\x18\x03 \x03(\x0b\x32\x37.google.cloud.automl.v1beta1.PredictRequest.ParamsEntry\x1a-\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xd1\x01\n\x0fPredictResponse\x12?\n\x07payload\x18\x01 \x03(\x0b\x32..google.cloud.automl.v1beta1.AnnotationPayload\x12L\n\x08metadata\x18\x02 \x03(\x0b\x32:.google.cloud.automl.v1beta1.PredictResponse.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32\xbe\x01\n\x11PredictionService\x12\xa8\x01\n\x07Predict\x12+.google.cloud.automl.v1beta1.PredictRequest\x1a,.google.cloud.automl.v1beta1.PredictResponse\"B\x82\xd3\xe4\x93\x02<\"7/v1beta1/{name=projects/*/locations/*/models/*}:predict:\x01*B~\n\x1f\x63om.google.cloud.automl.v1beta1B\x16PredictionServiceProtoP\x01ZAgoogle.golang.org/genproto/googleapis/cloud/automl/v1beta1;automlb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_cloud_dot_automl__v1beta1_dot_proto_dot_annotation__payload__pb2.DESCRIPTOR,google_dot_cloud_dot_automl__v1beta1_dot_proto_dot_data__items__pb2.DESCRIPTOR,])




_PREDICTREQUEST_PARAMSENTRY = _descriptor.Descriptor(
  name='ParamsEntry',
  full_name='google.cloud.automl.v1beta1.PredictRequest.ParamsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.cloud.automl.v1beta1.PredictRequest.ParamsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='google.cloud.automl.v1beta1.PredictRequest.ParamsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=401,
  serialized_end=446,
)

_PREDICTREQUEST = _descriptor.Descriptor(
  name='PredictRequest',
  full_name='google.cloud.automl.v1beta1.PredictRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='google.cloud.automl.v1beta1.PredictRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload', full_name='google.cloud.automl.v1beta1.PredictRequest.payload', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='params', full_name='google.cloud.automl.v1beta1.PredictRequest.params', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PREDICTREQUEST_PARAMSENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=234,
  serialized_end=446,
)


_PREDICTRESPONSE_METADATAENTRY = _descriptor.Descriptor(
  name='MetadataEntry',
  full_name='google.cloud.automl.v1beta1.PredictResponse.MetadataEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.cloud.automl.v1beta1.PredictResponse.MetadataEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='google.cloud.automl.v1beta1.PredictResponse.MetadataEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=611,
  serialized_end=658,
)

_PREDICTRESPONSE = _descriptor.Descriptor(
  name='PredictResponse',
  full_name='google.cloud.automl.v1beta1.PredictResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='payload', full_name='google.cloud.automl.v1beta1.PredictResponse.payload', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='google.cloud.automl.v1beta1.PredictResponse.metadata', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PREDICTRESPONSE_METADATAENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=449,
  serialized_end=658,
)

_PREDICTREQUEST_PARAMSENTRY.containing_type = _PREDICTREQUEST
_PREDICTREQUEST.fields_by_name['payload'].message_type = google_dot_cloud_dot_automl__v1beta1_dot_proto_dot_data__items__pb2._EXAMPLEPAYLOAD
_PREDICTREQUEST.fields_by_name['params'].message_type = _PREDICTREQUEST_PARAMSENTRY
_PREDICTRESPONSE_METADATAENTRY.containing_type = _PREDICTRESPONSE
_PREDICTRESPONSE.fields_by_name['payload'].message_type = google_dot_cloud_dot_automl__v1beta1_dot_proto_dot_annotation__payload__pb2._ANNOTATIONPAYLOAD
_PREDICTRESPONSE.fields_by_name['metadata'].message_type = _PREDICTRESPONSE_METADATAENTRY
DESCRIPTOR.message_types_by_name['PredictRequest'] = _PREDICTREQUEST
DESCRIPTOR.message_types_by_name['PredictResponse'] = _PREDICTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PredictRequest = _reflection.GeneratedProtocolMessageType('PredictRequest', (_message.Message,), dict(

  ParamsEntry = _reflection.GeneratedProtocolMessageType('ParamsEntry', (_message.Message,), dict(
    DESCRIPTOR = _PREDICTREQUEST_PARAMSENTRY,
    __module__ = 'google.cloud.automl_v1beta1.proto.prediction_service_pb2'
    # @@protoc_insertion_point(class_scope:google.cloud.automl.v1beta1.PredictRequest.ParamsEntry)
    ))
  ,
  DESCRIPTOR = _PREDICTREQUEST,
  __module__ = 'google.cloud.automl_v1beta1.proto.prediction_service_pb2'
  ,
  __doc__ = """Request message for
  [PredictionService.Predict][google.cloud.automl.v1beta1.PredictionService.Predict].
  
  
  Attributes:
      name:
          Name of the model requested to serve the prediction.
      payload:
          Required. Payload to perform a prediction on. The payload must
          match the problem type that the model was trained to solve.
      params:
          Additional domain-specific parameters, any string must be up
          to 25000 characters long.  -  For Translation:
          ``translation_allow_fallback`` - If specified, AutoML will
          fallback to use a Google translation model for translation
          requests if the the specified AutoML translation model cannot
          serve the request. The [PredictResponse.metadata][google.cloud
          .automl.v1beta1.PredictResponse.metadata] field provides
          additional data to the caller.  -  For Image Classification:
          ``score_threshold`` - (float) A value from 0.0 to 1.0. When
          the model makes predictions for an image, it will only produce
          results that have at least this confidence score threshold.
          The default is 0.5.
  """,
  # @@protoc_insertion_point(class_scope:google.cloud.automl.v1beta1.PredictRequest)
  ))
_sym_db.RegisterMessage(PredictRequest)
_sym_db.RegisterMessage(PredictRequest.ParamsEntry)

PredictResponse = _reflection.GeneratedProtocolMessageType('PredictResponse', (_message.Message,), dict(

  MetadataEntry = _reflection.GeneratedProtocolMessageType('MetadataEntry', (_message.Message,), dict(
    DESCRIPTOR = _PREDICTRESPONSE_METADATAENTRY,
    __module__ = 'google.cloud.automl_v1beta1.proto.prediction_service_pb2'
    # @@protoc_insertion_point(class_scope:google.cloud.automl.v1beta1.PredictResponse.MetadataEntry)
    ))
  ,
  DESCRIPTOR = _PREDICTRESPONSE,
  __module__ = 'google.cloud.automl_v1beta1.proto.prediction_service_pb2'
  ,
  __doc__ = """Response message for
  [PredictionService.Predict][google.cloud.automl.v1beta1.PredictionService.Predict].
  
  Currently, this is only used to return an image recognition prediction
  result. More prediction output metadata might be introduced in the
  future.
  
  
  Attributes:
      payload:
          Prediction result.
      metadata:
          Additional domain-specific prediction response metadata. \*
          For Translation:  ``translation_fallback_model`` - When [Predi
          ctRequest.params][google.cloud.automl.v1beta1.PredictRequest.p
          arams] has ``translation_allow_fallback`` specified, the
          caller can check the value of ``translation_fallback_model``
          in the metadata to determine whether a translation fallback
          model was used and which model was used.
  """,
  # @@protoc_insertion_point(class_scope:google.cloud.automl.v1beta1.PredictResponse)
  ))
_sym_db.RegisterMessage(PredictResponse)
_sym_db.RegisterMessage(PredictResponse.MetadataEntry)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\037com.google.cloud.automl.v1beta1B\026PredictionServiceProtoP\001ZAgoogle.golang.org/genproto/googleapis/cloud/automl/v1beta1;automl'))
_PREDICTREQUEST_PARAMSENTRY.has_options = True
_PREDICTREQUEST_PARAMSENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
_PREDICTRESPONSE_METADATAENTRY.has_options = True
_PREDICTRESPONSE_METADATAENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))

_PREDICTIONSERVICE = _descriptor.ServiceDescriptor(
  name='PredictionService',
  full_name='google.cloud.automl.v1beta1.PredictionService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=661,
  serialized_end=851,
  methods=[
  _descriptor.MethodDescriptor(
    name='Predict',
    full_name='google.cloud.automl.v1beta1.PredictionService.Predict',
    index=0,
    containing_service=None,
    input_type=_PREDICTREQUEST,
    output_type=_PREDICTRESPONSE,
    options=_descriptor._ParseOptions(descriptor_pb2.MethodOptions(), _b('\202\323\344\223\002<\"7/v1beta1/{name=projects/*/locations/*/models/*}:predict:\001*')),
  ),
])
_sym_db.RegisterServiceDescriptor(_PREDICTIONSERVICE)

DESCRIPTOR.services_by_name['PredictionService'] = _PREDICTIONSERVICE

# @@protoc_insertion_point(module_scope)
