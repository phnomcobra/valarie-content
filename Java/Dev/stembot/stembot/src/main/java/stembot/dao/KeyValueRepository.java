package stembot;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface KeyValueRepository extends MongoRepository<KeyValue, String>, KeyValueRepositoryCustom {
    public KeyValue findByName(String name);
}