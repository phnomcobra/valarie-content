package stembot;

import java.util.List;
import java.util.UUID;

import org.json.JSONObject;
import org.json.JSONArray;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Autowired;

@Component
public class ScheduledTasks {
    @Autowired
    private PeerRepository peerRepository;
    
    @Autowired
    private RouteRepository routeRepository;
    
    @Autowired
    private MessageRepository messageRepository;
    
    @Autowired
    private KeyValueRepository keyValueRepository;
    
    @Autowired
    private CascadeRepository cascadeRepository;
    
    @Scheduled(fixedRate = 60000)
    public void expiration() {
        this.peerRepository.expirePeers();
        this.cascadeRepository.expireCascades();
        this.messageRepository.expireMessages(60);
    }
    
    @Scheduled(fixedRate = 15000)
    public void ageAndAdvertise() {
        this.routeRepository.ageRoutes(15, 3600);
        
        String agtuuid = this.keyValueRepository.getKeyValue("agtuuid", UUID.randomUUID().toString()).value;
        
        JSONObject advertisement = new JSONObject();
        
        advertisement.put("agtuuid", agtuuid);
        advertisement.put("type", new String("route advertisement"));
        
        JSONArray routesJson = new JSONArray();
        JSONObject routeJson;
        
        List<Route> routes = this.routeRepository.getRoutes();
        
        for(int i = 0; i < routes.size(); i++) {
            routeJson = new JSONObject();
            
            routeJson.put("agtuuid", routes.get(i).agtuuid);
            routeJson.put("weight", routes.get(i).weight);
            routeJson.put("gtwuuid", agtuuid);
            
            routesJson.put(routeJson);
        }
        
        List<String> peerAgtuuids = this.peerRepository.getAgtuuids();
        
        for(int i = 0; i < peerAgtuuids.size(); i++) {
            routeJson = new JSONObject();
            
            routeJson.put("agtuuid", peerAgtuuids.get(i));
            routeJson.put("weight", new Integer(0));
            routeJson.put("gtwuuid", agtuuid);
            
            routesJson.put(routeJson);
        }
        
        advertisement.put("routes", routesJson);
        
        for(int i = 0; i < peerAgtuuids.size(); i++) {
            advertisement.put("dest", peerAgtuuids.get(i));
            
            this.messageRepository.insert(new Message(peerAgtuuids.get(i), advertisement.toString()));
        }
    }
}