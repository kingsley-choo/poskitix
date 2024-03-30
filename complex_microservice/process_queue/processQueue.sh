SHELL=/bin/bash
curl -X POST "http://localhost:5200/queue/process" >> /var/log/cron.log 2>&1
