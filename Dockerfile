FROM python:3.11

WORKDIR /TransactionService

COPY requirements.txt requirements.txt

RUN pip install pip-tools
RUN pip-sync requirements.txt

COPY . .

RUN apt-get update && \
    apt-get install -y libpq-dev build-essential git-all


RUN chmod +x /TransactionService/entrypoint.sh
ENTRYPOINT ["/TransactionService/entrypoint.sh"]

CMD ["sh", "-c", "cd /TransactionService/src && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
