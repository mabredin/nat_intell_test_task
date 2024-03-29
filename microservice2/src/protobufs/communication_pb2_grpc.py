# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
from . import communication_pb2 as communication__pb2
import grpc


class CommunicatorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetBalance = channel.unary_unary(
            "/communication.Communicator/GetBalance",
            request_serializer=communication__pb2.BalanceRequest.SerializeToString,
            response_deserializer=communication__pb2.BalanceReply.FromString,
        )
        self.GetLatestBlock = channel.unary_unary(
            "/communication.Communicator/GetLatestBlock",
            request_serializer=communication__pb2.BlockRequest.SerializeToString,
            response_deserializer=communication__pb2.BlockReply.FromString,
        )
        self.VerifyAddress = channel.unary_unary(
            "/communication.Communicator/VerifyAddress",
            request_serializer=communication__pb2.VerifyAddressRequest.SerializeToString,
            response_deserializer=communication__pb2.VerifyAddressReply.FromString,
        )


class CommunicatorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetBalance(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetLatestBlock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def VerifyAddress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_CommunicatorServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetBalance": grpc.unary_unary_rpc_method_handler(
            servicer.GetBalance,
            request_deserializer=communication__pb2.BalanceRequest.FromString,
            response_serializer=communication__pb2.BalanceReply.SerializeToString,
        ),
        "GetLatestBlock": grpc.unary_unary_rpc_method_handler(
            servicer.GetLatestBlock,
            request_deserializer=communication__pb2.BlockRequest.FromString,
            response_serializer=communication__pb2.BlockReply.SerializeToString,
        ),
        "VerifyAddress": grpc.unary_unary_rpc_method_handler(
            servicer.VerifyAddress,
            request_deserializer=communication__pb2.VerifyAddressRequest.FromString,
            response_serializer=communication__pb2.VerifyAddressReply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "communication.Communicator", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Communicator(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetBalance(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/communication.Communicator/GetBalance",
            communication__pb2.BalanceRequest.SerializeToString,
            communication__pb2.BalanceReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetLatestBlock(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/communication.Communicator/GetLatestBlock",
            communication__pb2.BlockRequest.SerializeToString,
            communication__pb2.BlockReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def VerifyAddress(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/communication.Communicator/VerifyAddress",
            communication__pb2.VerifyAddressRequest.SerializeToString,
            communication__pb2.VerifyAddressReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
