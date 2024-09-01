#!/bin/bash
cd ..
source during/bin/activate
cd during-ai
gunicorn -k uvicorn.workers.UvicornWorker -w 4 --bind 0.0.0.0:3142 main:app