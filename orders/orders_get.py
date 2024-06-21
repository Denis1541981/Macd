#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import uuid
from dotenv import load_dotenv, find_dotenv
import logging
import os
from tinkoff.invest import Client, RequestError, OrderType, PriceType, OrderDirection, PostOrderResponse
from Instruments.uid_share_info import get_uid_info

load_dotenv(find_dotenv())

TOKEN = os.getenv("TOKEN_FULL")
ACCOUNT_ID = os.getenv("ACCOUNT_ID_TEST")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("Operations.log", mode="a")
logger.addHandler(file_handler)
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_buy_order(figi, quantity, AccountID):
    uid = get_uid_info(figi=figi)  # uid
    order_id = str(uuid.uuid4().hex)
    with Client(TOKEN) as client:
        try:
            order = client.orders.post_order(
                figi=figi,
                quantity=quantity,
                direction=OrderDirection.ORDER_DIRECTION_BUY,
                account_id=AccountID,
                order_type=OrderType.ORDER_TYPE_BESTPRICE,
                order_id=order_id,
                instrument_id=uid,
                price_type=PriceType.PRICE_TYPE_CURRENCY
            )
            logging.info(order)
            x = response_to_dict(order)
            logging.info(x)
            return order_id
        except RequestError as e:
            logging.error(e.details)
        except Exception as e:
            logging.error(f"post order error: {e}")


def get_sell_order(figi, quantity, AccountID):
    uid = get_uid_info(figi=figi)
    order_id = str(uuid.uuid4().hex)
    with Client(TOKEN) as client:
        try:
            order = client.orders.post_order(
                figi=figi,
                quantity=quantity,
                direction=OrderDirection.ORDER_DIRECTION_SELL,
                account_id=AccountID,
                order_type=OrderType.ORDER_TYPE_BESTPRICE,
                order_id=order_id,
                instrument_id=uid,
                price_type=PriceType.PRICE_TYPE_CURRENCY
            )
            logging.info(order)
            x = response_to_dict(order)
            logging.info(x)
            return x
        except RequestError as e:
            logging.error(f"post order error: {e}")
        except Exception as e:
            logging.error(f"post order error: {e}")


def response_to_dict(response: PostOrderResponse):
    try:
        response_dict = {}
        order = response
        order_id = order.order_id
        execution_report_status = order.execution_report_status
        lots_requested = order.lots_requested
        lots_executed = order.lots_executed
        initial_order_price = order.initial_order_price.units + order.initial_order_price.nano / 1e9
        total_order_amount = order.total_order_amount.units + order.total_order_amount.nano / 1e9
        direction = order.direction
        order_type = order.order_type
        message = order.message
        instrument_uid = order.instrument_uid
        order_request_id = order.order_request_id
        response_metadata_tracking_id = order.response_metadata.tracking_id
        response_metadata_server_time = order.response_metadata.server_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        response_dict['order_id'] = {
            "order_id": order_id,
            "execution_report_status": execution_report_status,
            "lots_requested": lots_requested,
            "lots_executed": lots_executed,
            "initial_order_price": initial_order_price,
            "total_order_amount": total_order_amount,
            "direction": direction,
            "order_type": order_type,
            "message": message,
            "instrument_uid": instrument_uid,
            "order_request_id": order_request_id,
            "response_metadata_tracking_id": response_metadata_tracking_id,
            "response_metadata_server_time": response_metadata_server_time,

        }
        logging.info(response_dict)
        with open(f"/home/den/PycharmProjects/tink_exemple/robot/Temp/Order_{order_id}.json", "w") as f:
            json.dump(response_dict, f, indent=4, ensure_ascii=False)
        return response_dict
    except Exception as e:
        logging.error(e)


def main():
    logging.basicConfig(level=logging.INFO)
    figi = "BBG004731354"
    quantity = 1
    get_buy_order(figi=figi, quantity=quantity, AccountID=ACCOUNT_ID)
    get_sell_order(figi=figi, quantity=quantity, AccountID=ACCOUNT_ID)


if __name__ == '__main__':
    main()