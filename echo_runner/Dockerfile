FROM python:3.11
WORKDIR /atelier

COPY ./requirements.txt /atelier/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /atelier/requirements.txt

COPY ./packages/echo_runner /atelier/echo_runner

CMD ["python3", "-m", "echo_runner.main"]
