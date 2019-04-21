package stembot;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface CascadeRepository extends MongoRepository<Cascade, String>, CascadeRepositoryCustom {
}