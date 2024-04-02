# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: health.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0chealth.proto\x12\x10\x44puHealthService\"\x0f\n\rEepromRequest\"\xb4\x02\n\x0e\x45\x65promResponse\x12\x0f\n\x07slot_id\x18\x01 \x01(\t\x12;\n\x06header\x18\x02 \x01(\x0b\x32+.DpuHealthService.EepromResponse.HeaderInfo\x12@\n\ttlvfields\x18\x03 \x03(\x0b\x32-.DpuHealthService.EepromResponse.TlvFieldInfo\x12\x0f\n\x07success\x18\x04 \x01(\x08\x1a\x39\n\nHeaderInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x0e\n\x06length\x18\x03 \x01(\t\x1a\x46\n\x0cTlvFieldInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0b\n\x03len\x18\x03 \x01(\t\x12\r\n\x05value\x18\x04 \x01(\t\"\x0f\n\rStatusRequest\"\xfb\x05\n\x0eStatusResponse\x12\x0f\n\x07slot_id\x18\x01 \x01(\t\x12=\n\x07summary\x18\x02 \x01(\x0b\x32,.DpuHealthService.StatusResponse.SummaryInfo\x12=\n\x08statuses\x18\x03 \x03(\x0b\x32+.DpuHealthService.StatusResponse.StatusInfo\x12\x0f\n\x07success\x18\x04 \x01(\x08\x1a\xa1\x02\n\x0bSummaryInfo\x12\x12\n\nled_status\x18\x01 \x01(\t\x12L\n\x0fservices_status\x18\x02 \x01(\x0e\x32\x33.DpuHealthService.StatusResponse.SummaryInfo.Status\x12\x13\n\x0bnot_running\x18\x03 \x01(\t\x12\x16\n\x0enot_accessible\x18\x04 \x01(\t\x12L\n\x0fhardware_status\x18\x05 \x01(\x0e\x32\x33.DpuHealthService.StatusResponse.SummaryInfo.Status\x12\x17\n\x0fhardware_reason\x18\x06 \x01(\t\"\x1c\n\x06Status\x12\x06\n\x02OK\x10\x00\x12\n\n\x06NOT_OK\x10\x01\x1a\xa4\x02\n\nStatusInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x42\n\x06status\x18\x02 \x01(\x0e\x32\x32.DpuHealthService.StatusResponse.StatusInfo.Status\x12>\n\x04type\x18\x03 \x01(\x0e\x32\x30.DpuHealthService.StatusResponse.StatusInfo.Type\"\x1c\n\x06Status\x12\x06\n\x02OK\x10\x00\x12\n\n\x06NOT_OK\x10\x01\"f\n\x04Type\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06SYSTEM\x10\x01\x12\x0b\n\x07PROCESS\x10\x02\x12\x0e\n\nFILESYSTEM\x10\x03\x12\x0b\n\x07PROGRAM\x10\x04\x12\x0b\n\x07SERVICE\x10\x05\x12\x0e\n\nUSERDEFINE\x10\x06\"W\n\x0bRebootCause\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05\x63\x61use\x18\x02 \x01(\t\x12\x0c\n\x04user\x18\x03 \x01(\t\x12\x0f\n\x07\x63omment\x18\x04 \x01(\t\x12\x0c\n\x04time\x18\x05 \x01(\t\"m\n\x13RebootCauseResponse\x12\x0f\n\x07slot_id\x18\x01 \x01(\t\x12\x34\n\rreboot_causes\x18\x02 \x03(\x0b\x32\x1d.DpuHealthService.RebootCause\x12\x0f\n\x07success\x18\x03 \x01(\x08\"\x14\n\x12RebootCauseRequest2\x8b\x02\n\tHealthSvc\x12N\n\tGetEeprom\x12\x1f.DpuHealthService.EepromRequest\x1a .DpuHealthService.EepromResponse\x12N\n\tGetHealth\x12\x1f.DpuHealthService.StatusRequest\x1a .DpuHealthService.StatusResponse\x12^\n\x0fGetRebootCauses\x12$.DpuHealthService.RebootCauseRequest\x1a%.DpuHealthService.RebootCauseResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'health_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_EEPROMREQUEST']._serialized_start=34
  _globals['_EEPROMREQUEST']._serialized_end=49
  _globals['_EEPROMRESPONSE']._serialized_start=52
  _globals['_EEPROMRESPONSE']._serialized_end=360
  _globals['_EEPROMRESPONSE_HEADERINFO']._serialized_start=231
  _globals['_EEPROMRESPONSE_HEADERINFO']._serialized_end=288
  _globals['_EEPROMRESPONSE_TLVFIELDINFO']._serialized_start=290
  _globals['_EEPROMRESPONSE_TLVFIELDINFO']._serialized_end=360
  _globals['_STATUSREQUEST']._serialized_start=362
  _globals['_STATUSREQUEST']._serialized_end=377
  _globals['_STATUSRESPONSE']._serialized_start=380
  _globals['_STATUSRESPONSE']._serialized_end=1143
  _globals['_STATUSRESPONSE_SUMMARYINFO']._serialized_start=559
  _globals['_STATUSRESPONSE_SUMMARYINFO']._serialized_end=848
  _globals['_STATUSRESPONSE_SUMMARYINFO_STATUS']._serialized_start=820
  _globals['_STATUSRESPONSE_SUMMARYINFO_STATUS']._serialized_end=848
  _globals['_STATUSRESPONSE_STATUSINFO']._serialized_start=851
  _globals['_STATUSRESPONSE_STATUSINFO']._serialized_end=1143
  _globals['_STATUSRESPONSE_STATUSINFO_STATUS']._serialized_start=820
  _globals['_STATUSRESPONSE_STATUSINFO_STATUS']._serialized_end=848
  _globals['_STATUSRESPONSE_STATUSINFO_TYPE']._serialized_start=1041
  _globals['_STATUSRESPONSE_STATUSINFO_TYPE']._serialized_end=1143
  _globals['_REBOOTCAUSE']._serialized_start=1145
  _globals['_REBOOTCAUSE']._serialized_end=1232
  _globals['_REBOOTCAUSERESPONSE']._serialized_start=1234
  _globals['_REBOOTCAUSERESPONSE']._serialized_end=1343
  _globals['_REBOOTCAUSEREQUEST']._serialized_start=1345
  _globals['_REBOOTCAUSEREQUEST']._serialized_end=1365
  _globals['_HEALTHSVC']._serialized_start=1368
  _globals['_HEALTHSVC']._serialized_end=1635
# @@protoc_insertion_point(module_scope)
