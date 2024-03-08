import dotenv from '@dotenvx/dotenvx';
import nodemailer from 'nodemailer';

dotenv.config();

const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: process.env.email,
      pass: process.env.email_password
    },
  });

  // async..await is not allowed in global scope, must use a wrapper
async function main() {
    // send mail with defined transport object
    const info = await transporter.sendMail({
      from: process.env.email,
      to: "germainegoh.2022@scis.smu.edu.sg, gxlee.2022@scis.smu.edu.sg", // list of receivers
      subject: "Hello ✔", // Subject line
      text: "Hello world? ESD", // plain text body
      html: "<b>Hello world? ESD</b>", // html body
    });
  
    console.log("Message sent: %s", info.messageId);
    // Message sent: <d786aa62-4e0a-070a-47ed-0b0666549519@ethereal.email>
  }
  
  main().catch(console.error);