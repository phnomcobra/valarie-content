package stembot;

import org.springframework.data.annotation.Id;

public class Route {
    @Id
    public String id;
    
    public String agtuuid;
    public String gtwuuid;
    public Integer weight;
    
    public Route(String agtuuid, String gtwuuid, Integer weight) {
        this.agtuuid = agtuuid;
        this.gtwuuid = gtwuuid;
        this.weight = weight;
    }
}