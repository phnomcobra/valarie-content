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
public class CascadeRepositoryCustomImpl implements CascadeRepositoryCustom {
    @Autowired
    MongoTemplate mongoTemplate;
    
    @Override
    public boolean touchCascade(String cscuuid) {
        Cascade cascade;
        Boolean isNew = new Boolean(true);
        
        Query query = new Query(Criteria.where("cscuuid").is(cscuuid));

        List<Cascade> cascades = this.mongoTemplate.find(query, Cascade.class);
        
        if(cascades.size() > 0) {
            isNew = false;
        } else {
            cascade = new Cascade(cscuuid);

            this.mongoTemplate.insert(cascade);
        }
        
        return isNew;
    }
    
    @Override 
    public void expireCascades() {
        Instant instant = Instant.now();
        Long currentTime = new Long(instant.getEpochSecond());
        
        Query query = new Query(Criteria.where("destroyTime").lt(currentTime));
        
        this.mongoTemplate.remove(query, Cascade.class);
    }
}