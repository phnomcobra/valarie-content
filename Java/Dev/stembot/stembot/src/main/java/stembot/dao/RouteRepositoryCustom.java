package stembot;

import java.util.List;

public interface RouteRepositoryCustom  {
    public void touchRoute(String agtuuid, String gtwuuid, Integer weight);
    public void ageRoutes(Integer age, Integer maxAge);
    public String getGtwuuid(String agtuuid);
    public List<Route> getRoutes();
}