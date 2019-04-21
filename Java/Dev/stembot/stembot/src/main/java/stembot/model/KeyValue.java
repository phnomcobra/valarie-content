package stembot;

import org.springframework.data.annotation.Id;

public class KeyValue {
    @Id
    public String id;

    public String name;
    public String value;
    
    public KeyValue(String name, String value) {
        this.name = name;
        this.value = value;
    }
}