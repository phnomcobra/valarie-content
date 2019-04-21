package stembot;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface PeerRepository extends MongoRepository<Peer, String>, PeerRepositoryCustom {
}