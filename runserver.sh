#!/bin/bash

gunicorn -w 1 -t 24 -b 0.0.0.0:8000 --error-logfile - --log-file - config.wsgi
