import os

import requests
from loguru import logger

from ratatosk_errands.adapter import Rabbit
from ratatosk_errands.model import Echo

host = os.getenv("RABBIT_HOST")
port = int(os.getenv("RABBIT_PORT"))
username = os.getenv("RABBIT_USERNAME")
password = os.getenv("RABBIT_PASSWORD")


def receive_echo(channel, method, properties, body):
    try:
        logger.info(f"( ) receiving echo: {body}")
        echo = Echo.model_validate_json(body)
        requests.post(f"http://{echo.errand.destination}/receive_echo", json=echo.model_dump_json())
        channel.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"(*) relayed echo: {body}")
    except Exception as error:
        logger.error(f"(!) echo failed with error: {error}")


def main():
    with Rabbit(host, port, username, password) as rabbit:
        rabbit.channel.basic_qos(prefetch_count=1)
        rabbit.channel.queue_declare(queue="echo")
        rabbit.channel.basic_consume(queue="echo", on_message_callback=receive_echo)
        logger.info(f"setup complete, listening for echos")
        rabbit.channel.start_consuming()


if __name__ == '__main__':
    main()
