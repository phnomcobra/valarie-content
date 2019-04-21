package stembot;
 
import java.util.List;
import java.time.Instant;
 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Repository;
 
@Repository
public class RouteRepositoryCustomImpl implements RouteRepositoryCustom {
    @Autowired
    MongoTemplate mongoTemplate;
    
    @Override
    public void touchRoute(String agtuuid, String gtwuuid, Integer weight) {
        Route route;
        
        Query query = new Query(Criteria.where("agtuuid").is(agtuuid).and("gtwuuid").is(gtwuuid));

        List<Route> routes = this.mongoTemplate.find(query, Route.class);
        
        if(routes.size() > 1) {
            this.mongoTemplate.remove(query);

            route = new Route(agtuuid, gtwuuid, weight);

            this.mongoTemplate.insert(route);
        } else if(routes.size() == 1) {
            route = routes.get(0);
            
            if(route.weight > weight) {
                Update update = new Update().set("weight", weight);
            
                this.mongoTemplate.upsert(query, update, Route.class);
            }
        } else {
            route = new Route(agtuuid, gtwuuid, weight);

            this.mongoTemplate.insert(route);
        }
    }
    
    @Override
    public String getGtwuuid(String agtuuid) {
        String gtwuuid = null;
        
        Query query = new Query(Criteria.where("agtuuid").is(agtuuid));
        
        Sort sort = new Sort(Sort.Direction.ASC, "weight");

        Route route = this.mongoTemplate.findOne(query.with(sort), Route.class);
        
        if(route != null) {
            gtwuuid = new String(route.gtwuuid);
        }
        
        return gtwuuid;
    }
    
    @Override 
    public void ageRoutes(Integer age, Integer maxAge) {
        Update update;
        Query query;
        
        update = new Update().inc("weight", age);
        query = new Query(Criteria.where("weight").lte(maxAge));
        this.mongoTemplate.updateMulti(query, update, Route.class);

        query = new Query(Criteria.where("weight").gt(maxAge));
        this.mongoTemplate.remove(query, Route.class);
    }
    
    @Override                                                                   
    public List<Route> getRoutes() {  
        List<Route> routes = this.mongoTemplate.findAll(Route.class);

        return routes;
    }
}