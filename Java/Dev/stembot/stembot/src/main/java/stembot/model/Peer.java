package stembot;

import java.time.Instant;

import org.springframework.data.annotation.Id;

public class Peer {
    @Id
    public String id;
    
    public String agtuuid;
    public Long destroyTime;
    
    public Peer(String agtuuid) {
        this.agtuuid = agtuuid;
        
        Instant instant = Instant.now();
        this.destroyTime = new Long(instant.getEpochSecond() + 60);
    }
}