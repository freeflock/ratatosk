import os

from fastapi import FastAPI

from ratatosk_errands.adapter import Rabbit
from ratatosk_errands.model import Errand

host = os.getenv("RABBIT_HOST")
port = int(os.getenv("RABBIT_PORT"))
username = os.getenv("RABBIT_USERNAME")
password = os.getenv("RABBIT_PASSWORD")
app = FastAPI()


@app.post("/give_errand")
async def give_errand(errand: Errand):
    with Rabbit(host, port, username, password) as rabbit:
        rabbit.channel.queue_declare(queue="errand")
        rabbit.channel.basic_publish(exchange="", routing_key="errand", body=errand.model_dump_json())
