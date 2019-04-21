package stembot;

import java.util.List;

public interface CascadeRepositoryCustom  {
    public boolean touchCascade(String cscuuid);
    public void expireCascades();
}