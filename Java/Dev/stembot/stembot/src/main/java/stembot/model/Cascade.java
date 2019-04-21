package stembot;

import java.time.Instant;

import org.springframework.data.annotation.Id;

public class Cascade {
    @Id
    public String id;
    
    public String cscuuid;
    public Long destroyTime;

    public Cascade(String cscuuid) {
        this.cscuuid = cscuuid;
        
        Instant instant = Instant.now();
        this.destroyTime = new Long(instant.getEpochSecond() + 60);
    }
}