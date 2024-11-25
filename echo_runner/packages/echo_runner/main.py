import os
import traceback
from time import sleep

import requests
from loguru import logger

from ratatosk_errands.adapter import Rabbit
from ratatosk_errands.model import Echo

host = os.getenv("RABBIT_HOST")
port = int(os.getenv("RABBIT_PORT"))
username = os.getenv("RABBIT_USERNAME")
password = os.getenv("RABBIT_PASSWORD")
API_KEY = os.getenv("API_KEY")


def receive_echo(channel, method, properties, body):
    try:
        logger.info(f"( ) receiving echo: {body}")
        echo = Echo.model_validate_json(body)
        headers = {"x-api-key": API_KEY}
        response = requests.post(f"http://{echo.errand.destination}", headers=headers, json=echo.model_dump())
        if response.status_code != 200:
            raise RuntimeError(f"bad status code when relaying echo: <{response.status_code}> {response.text}")
        logger.info(f"(*) relayed echo: {body}")
    except Exception as error:
        logger.error(f"(!) echo failed with error: {error}\n{traceback.format_exc()}")
    finally:
        channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    while True:
        try:
            with Rabbit(host, port, username, password) as rabbit:
                rabbit.channel.basic_qos(prefetch_count=1)
                rabbit.channel.queue_declare(queue="echo")
                rabbit.channel.basic_consume(queue="echo", on_message_callback=receive_echo)
                logger.info(f"setup complete, listening for echos")
                rabbit.channel.start_consuming()
        except Exception as error:
            logger.error(f"(!) rabbit connection failed with error: {error}\n{traceback.format_exc()}")
            sleep(3)


if __name__ == '__main__':
    main()
