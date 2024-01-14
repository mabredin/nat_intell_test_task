import time
from concurrent import futures

import grpc

from config import GRPC_ADDRESS
from services import CommunicatorServicer, communication_pb2_grpc


def create_app():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    communication_pb2_grpc.add_CommunicatorServicer_to_server(
        CommunicatorServicer(), server
    )
    server.add_insecure_port(GRPC_ADDRESS)
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    create_app()
