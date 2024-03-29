FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./process_ticket.py .

RUN apt update
RUN apt install curl
RUN apt install cron

CMD [ "python", "./process_ticket.py" ]
