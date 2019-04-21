package stembot;

import org.json.JSONArray;

public interface MessageRepositoryCustom {
    public void expireMessages(Integer maxAge);
    public JSONArray pullMessages(String dest);
}