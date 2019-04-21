////////////////////////////////////////////////////////////////////////////////
// CLIENT
//
// Justin Dierking
// justin.l.dierking.mil@mail.mil
// justin.l.dierking.civ@mail.mil
// phnomcobra@gmail.com
//
// Gmail client for the gmail agent. Client runs logs into IMAP with
// credentials for a gmail account. Optional controls, subject
// filtering and trusted email addresses, can be set. Attachments are
// automatically downloaded into present working directory. Emails from
// untrusted addresses, if specified, are deleted. Emails from
// trusted emails are processed and then deleted.
//
// 03/14/2014 Original construction
// 04/12/2014 Added enableEmptyMailBox method
////////////////////////////////////////////////////////////////////////////////

package gmail.agent;

import java.io.*;
import java.util.*;
import javax.mail.BodyPart;
import javax.mail.Flags;
import javax.mail.Folder;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Multipart;
import javax.mail.Session;
import javax.mail.Store;
import javax.mail.Address;
import javax.mail.internet.*;

public class Client {
    /* Mutator method for setting username for logon */
    public void setUsername(String username) {
        this.username = username;
        
        // Set my address member
        try {
            this.myEmailAddress = new InternetAddress(username + "@gmail.com");
        } catch (AddressException e) {
            e.printStackTrace();
        }
    }
    
    /* Mutator method for setting password for logon */
    public void setPassword(String password) {
        this.password = password;
    }
   
    /* Mutator method for enabling the action of deleting all mail in mail box
       during reception.*/
    public void enableEmptyMailBox() {
        this.emptyMailBox = true;
    }
   
    /* Method for specifying trusted email addresses. If no addresses have been
    specified and the member is null, emails sent from all addresses are
    trusted. Trusted addressses are placed into an array/list. */
    public void addTrustedEmailAddress(String emailAddress) {
        if (trustedEmailAddresses == null) {
            trustedEmailAddresses = new ArrayList();
        }
        try {
            trustedEmailAddresses.add(new InternetAddress(emailAddress));
        } catch (AddressException e) {
            e.printStackTrace();
        }
    }
    
    /* Mutator method for setting the subject to filter for in an email. The 
    subject filter is type sensitive. */
    public void setSubjectFilter(String subjectFilter) {
        this.subjectFilter = subjectFilter;
    }
    
    /* Log into Gmail's IMAP. If successful, select the inbox folder and scan
    the subjects and from addresses for each email. If no subject filter is set
    or the subject matches the subject filter, the email's from address is
    checked against the trustedEmailAddresses list. If the list is null or the
    from address is trusted, the email is processed and then deleted from the 
    inbox. If the email is not trusted, the email is simply deleted. */
    public void receive() {
        // Set properties for session
        Properties props = new Properties();
        props.setProperty("mail.store.protocol", "imaps");
        
        try {
            // Start a session and connect to gmail
            Session session = Session.getDefaultInstance(props, null);
            Store store = session.getStore("imaps");
            store.connect("smtp.gmail.com", username + "@gmail.com", password);

            // Select the inbox
            Folder inbox = store.getFolder("inbox");
            inbox.open(Folder.READ_WRITE);
            
            // Get array of emails
            Message[] messages = inbox.getMessages();
            
            // Filter and process trusted emails
            for (int i = 0; i < messages.length; i++) {
                if (subjectFilter == null) {
                    if (trustedEmailAddresses == null) {
                        processMessageBody(messages[i]);
                    } else if (isEmailAddressTrusted(messages[i].getFrom()[0])) {
                        processMessageBody(messages[i]);
                    }
                    messages[i].setFlag(Flags.Flag.DELETED, true);
                } else if (messages[i].getSubject().equals(subjectFilter)) {
                    if (trustedEmailAddresses == null) {
                        processMessageBody(messages[i]);
                    } else if (isEmailAddressTrusted(messages[i].getFrom()[0])) {
                        processMessageBody(messages[i]);
                    }
                    messages[i].setFlag(Flags.Flag.DELETED, true);
                } else if (this.emptyMailBox) {
                    messages[i].setFlag(Flags.Flag.DELETED, true);
                }
            }
        
            // Close
            inbox.close(true);
            store.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    /* Private Members */
    private String username;
    private String password;
    private List<Address> trustedEmailAddresses;
    private String subjectFilter;
    private Address myEmailAddress;
    private Address replyEmailAddress;
    private boolean emptyMailBox = false;
    
    /* Check email address against list of trusted email address. If a match is
    found, return true for the email address is trusted. */
    private boolean isEmailAddressTrusted(Address emailAddress) {
        boolean trusted = false;
        
        for (int i = 0; i < trustedEmailAddresses.size(); i++) {
            if (emailAddress.equals(trustedEmailAddresses.get(i))) {
                trusted = true;
            }
        }
        
        return trusted;
    }
    
    /* Process the body of an email. Trap for instances of multipart blocks, 
    strings, and input streams. */
    private void processMessageBody(Message message) {
        try {
            Object content = message.getContent();

            replyEmailAddress = message.getFrom()[0];
            // check for string
            // then check for multipart
            // and then for input stream
            if (content instanceof String) {
                if (message.getContentType().startsWith("TEXT/PLAIN")) {
                    Execute.interpret(
                        content.toString(), 
                        replyEmailAddress, 
                        myEmailAddress,
                        "re: " + subjectFilter,
                        username, 
                        password);
                }
            } else if (content instanceof Multipart) {
                Multipart multiPart = (Multipart) content;
                procesMultiPart(multiPart);
            } else if (content instanceof InputStream) {
                InputStream inStream = (InputStream) content;
                int ch;
                while ((ch = inStream.read()) != -1) {
                    // System.out.write(ch);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (MessagingException e) {
            e.printStackTrace();
        }
    }
    
    /* Process the content of a multipart block of content. */
    private void procesMultiPart(Multipart content) {
        try {
            // Get the number of parts
            int multiPartCount = content.getCount();

            // For each part
            for (int i = 0; i < multiPartCount; i++) {
                BodyPart bodyPart = content.getBodyPart(i);
                Object o;
                o = bodyPart.getContent();

                // If the part is an attachment
                if ("ATTACHMENT".equalsIgnoreCase(bodyPart.getDisposition())) {
                    String destFilePath = bodyPart.getFileName();
 
                    FileOutputStream output = new FileOutputStream(destFilePath);
 
                    InputStream input = bodyPart.getInputStream();
 
                    byte[] buffer = new byte[4096];
 
                    int byteRead;
 
                    while ((byteRead = input.read(buffer)) != -1) {
                        output.write(buffer, 0, byteRead);
                    }
                    output.close();
                }
                
                // If part is a string
                if (o instanceof String) {
                    if (bodyPart.getContentType().startsWith("TEXT/PLAIN")) {
                        Execute.interpret(
                            o.toString(), 
                            replyEmailAddress, 
                            myEmailAddress, 
                            "re: " + subjectFilter,
                            username, 
                            password);
                    }
                // Else if part is a nested multipart
                } else if (o instanceof Multipart) {
                    procesMultiPart((Multipart) o);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (MessagingException e) {
            e.printStackTrace();
        }
    }
}
