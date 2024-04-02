# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import interrupt_pb2 as interrupt__pb2


class SystemSvcStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.InterruptGet = channel.unary_stream(
                '/pds.SystemSvc/InterruptGet',
                request_serializer=interrupt__pb2.InterruptGetRequest.SerializeToString,
                response_deserializer=interrupt__pb2.InterruptGetResponse.FromString,
                )


class SystemSvcServicer(object):
    """Missing associated documentation comment in .proto file."""

    def InterruptGet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SystemSvcServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'InterruptGet': grpc.unary_stream_rpc_method_handler(
                    servicer.InterruptGet,
                    request_deserializer=interrupt__pb2.InterruptGetRequest.FromString,
                    response_serializer=interrupt__pb2.InterruptGetResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'pds.SystemSvc', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SystemSvc(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def InterruptGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/pds.SystemSvc/InterruptGet',
            interrupt__pb2.InterruptGetRequest.SerializeToString,
            interrupt__pb2.InterruptGetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
