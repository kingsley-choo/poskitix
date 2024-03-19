import amqp from 'amqplib/callback_api.js';
import {transporter} from './send_email.js';
import emailTemplates from './templates.js';


amqp.connect(process.env.RABBIT_URL, function(error0, connection) {
  if (error0) {
    throw error0;
  }
  console.log('Connection to RabbitMQ Successful');
  connection.createChannel(function(error1, channel) {
    if (error1) {
      throw error1;
    }
    console.log('Channel created...');
    var exchange = 'email';

    channel.assertExchange(exchange, 'topic', {
      durable: true
    });
    console.log('Exchange asserted...');

    channel.assertQueue('', {
      exclusive: false // exclusive means used by only 1 connect and will be closed when connection is closed
      }, function(error2, q) {
        if (error2) {
          throw error2;
        }
        console.log(`Queue ${q.queue} created`);


      channel.bindQueue(q.queue, exchange, "*");
      console.log(`Queue ${q.queue} binded to *...`);


      channel.consume(q.queue,async  function(msg) {

        console.log("==Received message==")

        console.log('msg.content.toString :>> ', msg.content.toString());
        console.log('msg.fields.routingKey :>> ', msg.fields.routingKey);

        let msg_content = JSON.parse(msg.content.toString());
        let filled_email = await emailTemplates[msg.fields.routingKey](msg_content["user"],  msg_content["event"])

        await transporter.sendMail(filled_email)
        console.log("==Message sent==")

      }, {
        noAck: true
      });
    });

    channel.assertQueue('', {
        exclusive: false // exclusive means used by only 1 connect and will be closed when connection is closed
        }, function(error2, q) {
          if (error2) {
            throw error2;
          }
          console.log(`Queue ${q.queue} created`);
  
        channel.bindQueue(q.queue, exchange, "*.*");
        console.log(`Queue ${q.queue} binded to *.*...`);

        channel.consume(q.queue,async  function(msg) {
  
        if(msg.fields.routingKey != "ready.done"){
            console.log("==Received message==")
    
            console.log('msg.content.toString :>> ', msg.content.toString());
            console.log('msg.fields.routingKey :>> ', msg.fields.routingKey);

            let msg_content = JSON.parse(msg.content.toString());
    
            let filled_email = await emailTemplates[msg.fields.routingKey.replace(".", "_")](msg_content["user"], msg_content["event"])
    
            await transporter.sendMail(filled_email)
            console.log("==Message sent==")
        }
  
        }, {
          noAck: true
        });
      });


      channel.assertQueue('', {
        exclusive: false // exclusive means used by only 1 connect and will be closed when connection is closed
        }, function(error2, q) {
          if (error2) {
            throw error2;
          }
          console.log(`Queue ${q.queue} created`);
        channel.bindQueue(q.queue, exchange, "ready.done");
        console.log(`Queue ${q.queue} bind to ready.done....`);
        channel.consume(q.queue,async  function(msg) {
  
        console.log("==Received message buy ticket==")

        console.log('msg.content.toString :>> ', msg.content.toString());
        console.log('msg.fields.routingKey :>> ', msg.fields.routingKey);

        let msg_content = JSON.parse(msg.content.toString());

        let filled_email =  await emailTemplates[msg.fields.routingKey.replace(".", "_")](msg_content["user"], msg_content["event"],msg_content["ticket"])

        await transporter.sendMail(filled_email)
        console.log("==Message sent==")

  
        }, {
          noAck: true
        });
      });
  });
});



