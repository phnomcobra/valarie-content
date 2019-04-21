package stembot;
 
import java.util.List;
 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;
 
@Repository
public class KeyValueRepositoryCustomImpl implements KeyValueRepositoryCustom {
    @Autowired
    MongoTemplate mongoTemplate;

    @Override
    public KeyValue getKeyValue(String name) {
        return this.getKeyValue(name, new String(""));
    }
    
    @Override
    public KeyValue getKeyValue(String name, String defaultValue) {
        KeyValue keyValue;
        
        Query query = new Query(Criteria.where("name").is(name));

        List<KeyValue> keyValues = this.mongoTemplate.find(query, KeyValue.class);
        
        if(keyValues.size() > 1) {
            this.mongoTemplate.remove(query);

            keyValue = new KeyValue(name, defaultValue);

            this.mongoTemplate.insert(keyValue);
        } else if (keyValues.size() == 1) {
            keyValue = keyValues.get(0);
        } else {
            keyValue = new KeyValue(name, defaultValue);

            this.mongoTemplate.insert(keyValue);
        }

        return keyValue;
    }
}