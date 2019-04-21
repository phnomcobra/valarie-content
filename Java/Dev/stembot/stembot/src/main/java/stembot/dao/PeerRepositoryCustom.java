package stembot;

import java.util.List;

public interface PeerRepositoryCustom  {
    public Peer getPeer(String agtuuid);
    public void touchPeer(String agtuuid);
    public void expirePeers();
    public List<String> getAgtuuids();
}