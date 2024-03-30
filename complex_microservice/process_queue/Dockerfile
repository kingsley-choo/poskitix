FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./process_queue.py .

# update apt-get to install cron
RUN apt-get update && apt-get -y install cron && apt-get -y install curl
# copy shell script
COPY processQueue.sh ./
# provide permission to execute shell script
RUN chmod 775 ./processQueue.sh
# copy the cronjob that contains the command
COPY process_cron /etc/cron.d/process_cron
# provide execution rights
RUN chmod 644 /etc/cron.d/process_cron
# insert cronjob 
RUN crontab /etc/cron.d/process_cron
# to ensure cron is started successfully
RUN service cron start

# enable logging from cron
RUN touch /var/log/cron.log

CMD cron;python ./process_queue.py 
