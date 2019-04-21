package stembot;
 
import java.util.List;
import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONObject;

import java.time.Instant;
 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;
 
@Repository
public class MessageRepositoryCustomImpl implements MessageRepositoryCustom {
    @Autowired
    MongoTemplate mongoTemplate;
    
    @Override 
    public void expireMessages(Integer maxAge) {
        Instant instant = Instant.now();
        
        Long currentTime = new Long(instant.getEpochSecond());
        
        Query query = new Query(Criteria.where("timestamp").lt(currentTime - maxAge));
        
        this.mongoTemplate.remove(query, Message.class);
    }
    
    @Override
    public JSONArray pullMessages(String dest) {
        Instant instant;
        List<Message> messages;
        Long currentTime;
        Long initTime;
        
        JSONArray message = new JSONArray();
        
        Query query = new Query(Criteria.where("dest").is(dest));
        
        
        
        
        instant = Instant.now();
        initTime = new Long(instant.getEpochSecond());
        
        instant = Instant.now();
        currentTime = new Long(instant.getEpochSecond());
        
        messages = this.mongoTemplate.findAllAndRemove(query, Message.class);
        
        for(int i = 0; i < messages.size(); i++) {
            message.put(new JSONObject(messages.get(i).body));
        }
        
        
        
        
        while(currentTime - initTime < 5 && messages.size() == 0) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException ex) {
            }
            
            instant = Instant.now();
            currentTime = new Long(instant.getEpochSecond());
            
            messages = this.mongoTemplate.findAllAndRemove(query, Message.class);
            
            for(int i = 0; i < messages.size(); i++) {
                message.put(new JSONObject(messages.get(i).body));
            }
        }
        
        
        
        
        return message;
    }
}