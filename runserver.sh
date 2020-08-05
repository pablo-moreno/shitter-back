#!/bin/bash

uvicorn --workers 1 --host 0.0.0.0 --port 80 config.asgi:application
