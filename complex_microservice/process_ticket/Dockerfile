FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./process_ticket.py .

# update apt-get to install cron
RUN apt-get update && apt-get -y install cron && apt-get -y install curl
# copy the cronjob and the command we set 
COPY ticket_cron /etc/cron.d/ticket_cron
# provide execution rights
RUN chmod 0644 /etc/cron.d/ticket_cron
# insert cronjob 
RUN crontab /etc/cron.d/ticket_cron

# enable logging from cron
RUN touch /var/log/cron.log

CMD cron;python ./process_ticket.py 
