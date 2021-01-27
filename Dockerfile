FROM python:alpine
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT 1
ENV TZ 'America/Bogota'
RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime  \
    && echo $TZ >  /etc/timezone
WORKDIR /usr/src/app
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD uvicorn main:app --host 0.0.0.0 --debug --port $PORT --reload