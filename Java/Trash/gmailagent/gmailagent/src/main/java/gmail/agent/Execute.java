////////////////////////////////////////////////////////////////////////////////
// EXECUTE
//
// Justin Dierking
// justin.l.dierking.mil@mail.mil
// justin.l.dierking.civ@mail.mil
// phnomcobra@gmail.com
//
// Try to execute each command and buffer the redirected standard
// out stream and concatanate a response line by line. Once all 
// commands have been executed, send a reply consisting of multiple
// parts for each command. If a command is begins with attach, parse
// the remainder of the line as the filepath of an attachment and 
// attempt to attach the file.
//
// 03/14/2014 Original construction
// 03/17/2014 Added support for sending attachments
// 04/20/2014 Fixed null command
////////////////////////////////////////////////////////////////////////////////

package gmail.agent;

import java.util.Properties;
 
import javax.mail.Message;
import javax.mail.Address;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.*;
import javax.mail.Multipart;
import javax.activation.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.File;

public class Execute {
    public static void interpret(
        String systemCommands, 
        Address to,
        Address from,
        String subject,
        final String username, 
        final String password) {
      
        // Assuming you are sending email through relay.jangosmtp.net
        String host = "smtp.gmail.com";
        
        // Setup properties
        Properties props = new Properties();
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");
        props.put("mail.smtp.host", host);
        props.put("mail.smtp.port", "587");

        // Get the Session object.
        Session session = Session.getInstance(props,
        new javax.mail.Authenticator() {
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(username, password);
            }
        });

        try {
            // Create a default MimeMessage object.
            Message message = new MimeMessage(session);

            // Set From: header field of the header.
            message.setFrom(from);

            // Set To: header field of the header.
            message.setRecipient(Message.RecipientType.TO, to);

            // Split multiline commands by carriage return/linefeed
            String commands[] = systemCommands.split("\\r?\\n");
            
            // Create multipart
            Multipart multipart = new MimeMultipart();
            
            // Set subject
            message.setSubject(subject);
            
            /* Try to execute each command and buffer the redirected standard
            out stream and concatanate a response line by line. Once all 
            commands have been executed, send a reply consisting of multiple
            parts for each command. If a command is begins with attach, parse
            the remainder of the line as the filepath of an attachment and 
            attempt to attach the file. */
            for (int i = 0; i < commands.length; i++) {
                // Setup next part of the message body
                MimeBodyPart messageBodyPart = new MimeBodyPart();
                messageBodyPart = new MimeBodyPart();
                
                // Process the command and trap for the prefix "attach"
                if (commands[i].startsWith("attach")) {
                    String fileAttachment = commands[i].substring(7);
                    
                    if (fileExists(fileAttachment)) {
                        DataSource source = new FileDataSource(fileAttachment);
                        messageBodyPart.setDataHandler(new DataHandler(source));
                        messageBodyPart.setFileName(fileAttachment);
                    } else {
                        messageBodyPart.setText(fileAttachment + " does not exist!");
                    }
                } else if (commands[i] != null) {
                    messageBodyPart.setText(commands[i] + "\n" + runCommand(commands[i]));
                }
                
                // Add part
                multipart.addBodyPart(messageBodyPart);
            }
            
            // Put parts in message
            message.setContent(multipart);

            // Send the message
            Transport.send(message);
        } catch (MessagingException e) {
            e.printStackTrace();
        }
    }
    
    /* Run a command. Buffer the runtime's input stream line by line and return
    the output. If an exception is thrown, add the exception's message into
    the output. */
    private static String runCommand(String command) {
        String output = "";
        
        try {
            Runtime r = Runtime.getRuntime();
            Process p = r.exec(command);
            p.waitFor();
            
            BufferedReader b = new BufferedReader(new InputStreamReader(p.getInputStream()));
        
            String line = "";
            while ((line = b.readLine()) != null) {
                output = output + line + "\n";
            }
        }
        catch (InterruptedException e) {
            e.printStackTrace();
            output = output + e.getMessage() + "\n";
        }
        catch (IOException e) {
            e.printStackTrace();
            output = output + e.getMessage() + "\n";
        }
     
        return output;
    }
    
    /* Check to see if a file exists. */
    private static boolean fileExists(String filename) {
        boolean exists = false;
        File f = new File(filename);
        if(f.exists()) exists = true;
        return exists;
    }
}
