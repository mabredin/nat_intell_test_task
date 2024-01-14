from datetime import datetime

from fastapi import HTTPException
from starlette import status
from web3 import Web3

import schemas
from config import INFURA_ENDPOINT
from protobufs import communication_pb2, communication_pb2_grpc

w3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))


class CommunicatorServicer(communication_pb2_grpc.CommunicatorServicer):
    def GetBalance(self, request, context):
        reply = communication_pb2.BalanceReply()
        schema = get_balance_by_address(request.address)
        reply.balance = str(schema.balance)
        return reply

    def GetLatestBlock(self, request, context):
        reply = communication_pb2.BlockReply()
        schema = get_info_by_latest_block()
        reply.number = schema.number
        reply.count_transactions = schema.count_transactions
        reply.difficulty = schema.difficulty
        reply.time = schema.time
        return reply

    def VerifyAddress(self, request, context):
        reply = communication_pb2.VerifyAddressReply()
        schema = verify_address(request.address)
        reply.is_verified = schema.is_verified
        return reply


def get_balance_by_address(address: str) -> schemas.GetBalance:
    if not is_connected:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось подключиться к сети goerli",
        )
    balance = w3.eth.get_balance(address)
    balance = w3.from_wei(balance, "ether")
    return schemas.GetBalance(balance=balance)


def get_info_by_latest_block() -> schemas.GetInfoByBlock:
    if not is_connected:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось подключиться к сети goerli",
        )
    block = w3.eth.get_block("latest")
    formatted_time = datetime.utcfromtimestamp(block.timestamp).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
    return schemas.GetInfoByBlock(
        number=block.number,
        count_transactions=w3.eth.get_block_transaction_count(block.number),
        difficulty=block.difficulty,
        time=formatted_time,
    )


def verify_address(address: str) -> schemas.GetVerify:
    if not is_connected:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось подключиться к сети goerli",
        )

    is_address = check_is_address(address)
    is_contract = check_is_contract(address)
    is_verified = check_is_verified(is_address, is_contract)
    return schemas.GetVerify(is_verified=is_verified)


def is_connected(w3: Web3) -> bool:
    return w3.is_connected()


def check_is_address(address: str) -> bool:
    try:
        is_address = w3.is_address(address)
        return is_address
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Указанный адрес неверен или является контрактом",
        )


def check_is_contract(address: str) -> bool:
    try:
        result = w3.eth.get_code(address)
        return True if result else False
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Указанный адрес неверен или является контрактом",
        )


def check_is_verified(is_address: bool, is_contract: bool) -> bool:
    return True if is_address and not is_contract else False
