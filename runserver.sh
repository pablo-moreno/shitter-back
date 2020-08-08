#!/bin/bash

uvicorn --workers 1 --host 0.0.0.0 --port 8000 config.asgi:application
