export default  {
    waiting_ready : function(user_info,event_info) {
        return {
            from: process.env.email,
            to: user_info.email,
            subject: `You are ready to purchase ticket for ${event_info.eventname}`, // Subject line
            html: `<h2>Are you excited, ${user_info.username} because we are!</h2>
                        
                    <p>It is now your turn to purchase ticket for ${event_info.eventname} on ${event_info.date}</p>
                    
                    <p>Click <a href="${process.env.FRONTEND_URL}">here</a> to purchase. Hurry! you only have 15 minutes</p>`, // html body
          }
    },
    ready_missed : function(user_info,event_info) {
        return {
            from: process.env.email,
            to: user_info.email,
            subject: `You lost your spot in the queue for ${event_info.eventname}`, // Subject line
            html: `<h2>Oh no...you missed the chance</h2>
                        
                    <p>We regret to inform you that you are no longer able to purchase ticket for
                     ${event_info.eventname} on ${event_info.date} at ${event_info.location} as you failed to purchase within 15 minutes.
                     We do this to ensure everyone gets a fair chance for a ticket</p>
                    
                    <p>Thank you for your understanding</p>`, // html body
          }
    },
    waiting_fail : function(user_info,event_info) {
        return {
            from: process.env.email,
            to: user_info.email,
            subject: `${event_info.eventname} is sold out :(`, // Subject line
            html: `<h2>We are so sorry</h2>
                        
                    <p>
                        We regret to inform you that you are no longer able to purchase ticket for
                        ${event_info.eventname} on ${event_info.date} at ${event_info.location} as we have run out of tickets.
                        We sincerely apologise for any inconvenience.
                    </p>
                    
                    <p>Thank you for your understanding</p>`, // html body
          }
    },
    waiting : function(user_info,event_info) {
        return {
            from: process.env.email,
            to: user_info.email,
            subject: `You are in queue for ${event_info.eventname}`, // Subject line
            html: `<h2>You are on your way...</h2>
                        
                    <p>
                        You are now in queue for
                        ${event_info.eventname} on ${event_info.date} at ${event_info.location}.
                        We will notify you when you are ready to purchase tickets.
                    </p>
                    
                    <p>We are sorry but we do not have estimated waiting time</p>`, // html body
          }
    },
    ready_done : async function(user_info,event_info,ticket_info) {
        let url = await QRCode.toDataURL(ticket_info.tid);

        console.log(`<h2>Congratulations you got ticket for ${event_info.eventname}</h2>
                        
                    <p>
                        You have successfully purchased ticket for
                        ${event_info.eventname} on ${event_info.date} at ${event_info.location}.
                        Please arrive at least 15 minutes before the event and present the following barcode.
                    </p>

                    <p>
                        <img src=${url}/>
                    </p>
                    
                    <p>Hope you enjoy the concert!</p>`)

        return {
            from: process.env.email,
            to: user_info.email,
            subject: `Yay! You got the ticket for ${event_info.eventname}`, // Subject line
            html: `<h2>Congratulations you got ticket for ${event_info.eventname}</h2>
                        
                    <p>
                        You have successfully purchased ticket for
                        ${event_info.eventname} on ${event_info.date} at ${event_info.location}.
                        Please arrive at least 15 minutes before the event and present the following barcode.
                    </p>

                    <p>
                        <img src=${url}/>
                    </p>
                    
                    <p>Hope you enjoy the concert!</p>`, // html body
          }
    }


}