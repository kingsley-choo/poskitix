# IS213: Enterprise Solution Development: Poskitix 

## Requirements
```
- Docker Desktop
- Able to read english to follow the instructions below 
```

## Project Setup
Please follow the instructions before running the files

### Setting up of Kong of local machine
```
In Docker, install docker backup and share extension on docker hub from the below link
https://hub.docker.com/extensions/docker/volumes-backup-extension

Download poskitix_pgdata.tar.zst file from the submission folder

In Docker, click on Volumes Backup and Share extension, Import into new volume, and choose the downloaded poskitix_pgdata.tar.zst file in your local device, put Volume Name as poskitix_pgdata

Ensure that the 5 services can be seen in Kong manager at http://localhost:8002

Note: 
DO NOT RUN ‘docker compose down -d’ on command prompt after seeing the 5 services. 
Run ‘docker compose down’ instead.
```

## How to Run
On the file directory of the project, do the following:
```
$ docker compose build
$ docker compose up
```
# Service Overview

## Backstory
Concertgoers come across our service and decide to try out our service to book concert tickets as they’ve been disappointed with other sites in the past. They will be able to choose from a variety of events available (now and in the future) to queue for; and hopefully get their tickets. However they are not alone as they still have to compete with each other for those sweet, precious tickets. 

## Solution
A whole new Virtual Room for queueing that do not require users to stay on the webpage to queue. 

## Features
* Queue for multiple of your favourite events available
* Immediate notifications sent when your queue status is updated 
* Enjoy seamless payment with Stripe 

## Benefits
* Users no longer need to fear that they would miss out when it is their turn to buy
* Fair system - Ticket is guaranteed for users who enters the payment page! No more annoying "TICKET IS SOLD OUT" or "YOUR SELECTED TICKET HAS BEEN BOUGHT BY ANOTHER USER!" 
* Servers do not need to keep their connection alive with client webpages to update queue status - BIG COST SAVINGS!

## How to test the application
 + Login with User Email using the email found in from users.sql
 + Start Browsing Events
 + Choose Interested Event(s) to Queue for
 + Wait till Informed to Purchase Ticket (emails will be sent to users to notify you) 
 + Proceed to Pay by Clicking on Provided Link (“Waiting” will change to “Purchase Ticket”)
 + Receive your Ticket Details After Payment
 + Decide to Queue for Another Event or Leave the Page by Logging Out 


## Demo Video URL
Link -> https://youtu.be/ALFfOyGD9yc

