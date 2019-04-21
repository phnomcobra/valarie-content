////////////////////////////////////////////////////////////////////////////////
// AGENT
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
// 03/15/2014 Original construction
// 04/12/2014 Fixed remarks and added empty-mbx switch
// 04/14/2014 Added repeat switch
////////////////////////////////////////////////////////////////////////////////

package gmail.agent;

public class Agent {
    private static void help() {
	System.out.println("");
	System.out.println("Usage: java -jar Gmail_Agent.jar <username> <password> [OPTION]...");
	System.out.println("  --help       Displays this help and exit.");
	System.out.println("");
	System.out.println("Optional arguments.");
	System.out.println("  --subject    Set the subject to filter emails by.");
	System.out.println("  --trust      Add trusted email address to agent.");
	System.out.println("  --empty-mbx  Empty entire mailbox.");
	System.out.println("  --repeat     Check mailbox continuously after ? seconds.");
	System.out.println("");
    }
    
    public static void main(String[] args) {
        if (args.length > 1) {
            try {
                int repeat = 0;
                Client c = new Client();
            
                c.setUsername(args[0]);
                c.setPassword(args[1]);
            
                for (int i = 2; i < args.length - 1; i++) {
                    if (args[i].equalsIgnoreCase("--subject")) c.setSubjectFilter(args[i + 1]);
                    if (args[i].equalsIgnoreCase("--trust")) c.addTrustedEmailAddress(args[i + 1]);
                    if (args[i].equalsIgnoreCase("--repeat")) repeat = Integer.parseInt(args[i + 1]);
                }
            
                for (int i = 2; i < args.length; i++) {
                    if (args[i].equalsIgnoreCase("--empty-mbx")) c.enableEmptyMailBox();                
                }
            
                if (repeat > 0) {
                    while (1 == 1) {
                        c.receive();
                        Thread.sleep(repeat * 1000);
                    }
                } else c.receive();
            } catch (Exception e) {
            e.printStackTrace();
        }
            
        } else help();
    }    
}
