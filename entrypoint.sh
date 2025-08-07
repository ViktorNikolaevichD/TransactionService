#!/bin/bash

set -e

cd /TransactionService

alembic upgrade head

exec "$@"