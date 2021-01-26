FROM python:alpine
WORKDIR /usr/src/app
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD uvicorn main:app --host 0.0.0.0 --debug --port $PORT --reload