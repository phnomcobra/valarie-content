package stembot;

public interface KeyValueRepositoryCustom  {
    public KeyValue getKeyValue(String name);
    public KeyValue getKeyValue(String name, String defaultValue);
}