import os

from ratatosk_errands.adapter import Rabbit

host = os.getenv("RABBIT_HOST")
port = int(os.getenv("RABBIT_PORT"))
username = os.getenv("RABBIT_USERNAME")
password = os.getenv("RABBIT_PASSWORD")


def receive_reply(ch, method, properties, body):
    pass


def main():
    with Rabbit(host, port, username, password) as rabbit:
        rabbit.channel.queue_declare(queue="reply")
        rabbit.channel.basic_consume(queue="reply",
                                     auto_ack=True,
                                     on_message_callback=receive_reply)


if __name__ == '__main__':
    main()
