package stembot;
 
import java.util.List;
import java.util.ArrayList;

import java.time.Instant;
 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;
 
@Repository
public class PeerRepositoryCustomImpl implements PeerRepositoryCustom {
    @Autowired
    MongoTemplate mongoTemplate;
    
    @Override
    public void touchPeer(String agtuuid) {
        Instant instant = Instant.now();
        Long currentTime = new Long(instant.getEpochSecond());
        
        Peer peer = this.getPeer(agtuuid);
        
        if(peer.destroyTime - currentTime < 10) {
            Query query = new Query(Criteria.where("agtuuid").is(agtuuid));
            
            Update update = new Update().set("destroyTime", currentTime + 60);
            
            this.mongoTemplate.upsert(query, update, Peer.class);
        }
    }
    
    @Override 
    public void expirePeers() {
        Instant instant = Instant.now();
        Long currentTime = new Long(instant.getEpochSecond());
        
        Query query = new Query(Criteria.where("destroyTime").lt(currentTime));
        
        this.mongoTemplate.remove(query, Peer.class);
    }
    
    @Override
    public Peer getPeer(String agtuuid) {
        Peer peer;
        
        Query query = new Query(Criteria.where("agtuuid").is(agtuuid));

        List<Peer> peers = this.mongoTemplate.find(query, Peer.class);
        
        if(peers.size() > 1) {
            this.mongoTemplate.remove(query);

            peer = new Peer(agtuuid);

            this.mongoTemplate.insert(peer);
        } else if (peers.size() == 1) {
            peer = peers.get(0);
        } else {
            peer = new Peer(agtuuid);

            this.mongoTemplate.insert(peer);
        }
        
        return peer;
    }
    
    @Override                                                                   
    public List<String> getAgtuuids() {                                         
        List<Peer> peers = this.mongoTemplate.findAll(Peer.class);              
        List<String> agtuuids = new ArrayList<String>();                        
                                                                                
        for(Peer peer : peers) {                                                
            agtuuids.add(peer.agtuuid);                                         
        }                                                                       
                                                                                
        return agtuuids;                                                        
    }
}