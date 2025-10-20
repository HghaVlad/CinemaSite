#!/bin/sh
alembic upgrade head
exec fastapi run  main.py