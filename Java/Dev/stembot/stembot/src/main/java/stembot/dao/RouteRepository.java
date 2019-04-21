package stembot;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface RouteRepository extends MongoRepository<Peer, String>, RouteRepositoryCustom {
}