package stembot;

import java.time.Instant;

import org.springframework.data.annotation.Id;

public class Message {
    @Id
    public String id;
    
    public String dest;
    public Long timestamp;
    public String body;
    
    public Message(String dest, String body) {
        Instant instant = Instant.now();
        
        this.timestamp = new Long(instant.getEpochSecond());
        this.body = body;
        this.dest = dest;
    }
}