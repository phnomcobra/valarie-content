package stembot;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;

import org.springframework.beans.factory.annotation.Autowired;

import org.json.JSONObject;
import org.json.JSONArray;

import javax.servlet.http.HttpServletResponse;

import java.util.UUID;
import java.util.List;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.charset.StandardCharsets;

@RestController
public class Controller {
    private String secretDigestString;
    private String agtuuid;

    @Autowired
    private KeyValueRepository keyValueRepository;
    
    @Autowired
    private PeerRepository peerRepository;
    
    @Autowired
    private RouteRepository routeRepository;
    
    @Autowired
    private MessageRepository messageRepository;
    
    @Autowired
    private CascadeRepository cascadeRepository;
    
    private Controller() {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] encodedHash = digest.digest((byte[])("changeme").getBytes(StandardCharsets.UTF_8));
            this.secretDigestString = new String(this.bytesToHex(encodedHash).toString());
        } catch (java.security.NoSuchAlgorithmException e) {
        }
    }
    
    private static String bytesToHex(byte[] hash) {
        StringBuffer hexString = new StringBuffer();
        for (int i = 0; i < hash.length; i++) {
        String hex = Integer.toHexString(0xff & hash[i]);
        if(hex.length() == 1) hexString.append('0');
            hexString.append(hex);
        }
        return hexString.toString();
    }
    
    @RequestMapping("/mpi")
    public String mpi(@RequestBody String requestBody, @RequestHeader("Signature") String requestSignature, HttpServletResponse response) {
        String responseBody = new String();
        String responseSignature = new String();
        String computedSignature = new String();
        String messageType = new String();
        
        this.agtuuid = this.keyValueRepository.getKeyValue("agtuuid", UUID.randomUUID().toString()).value;
        
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            
            computedSignature = this.bytesToHex(digest.digest((this.secretDigestString + requestBody).getBytes(StandardCharsets.UTF_8)));
            
            if(computedSignature.equals(requestSignature)) {
                JSONObject requestObject = new JSONObject(requestBody);
                
                if(requestObject.has("isrc")) {
                    this.peerRepository.touchPeer(requestObject.getString("isrc"));
                } 
                
                if(requestObject.has("dest")) {
                    String dest = requestObject.getString("dest");
                    
                    if(dest.equals("")) {
                        requestObject.put("dest", this.agtuuid);
                    }
                } else {
                    requestObject.put("dest", this.agtuuid);
                }

                responseBody = this.process(requestObject);
                
                digest.reset();
                
                responseSignature = this.bytesToHex(digest.digest((this.secretDigestString + responseBody).getBytes(StandardCharsets.UTF_8)));
                
                response.setHeader("Signature", responseSignature);
            } else {
                response.setStatus(403);
                responseBody = "Signature Mismatch Detected!";
            }
        } catch (java.security.NoSuchAlgorithmException e) {
        }
        
        return responseBody;
    }
    
    public String process(JSONObject message) {
        String responseBody = new String();
        
        if(this.agtuuid.equals(message.getString("dest"))) {
            String type = message.getString("type");
            
            if(type.equals("create info event")) {
                message.put("info", new String("event"));
                responseBody = message.toString();
            } else if(type.equals("route advertisement")) {
                List<String> ignoredAgtuuids = this.peerRepository.getAgtuuids();
                
                // Add your own uuid to this list
                ignoredAgtuuids.add(this.agtuuid);

                JSONArray routes = message.getJSONArray("routes");
                for(int i = 0; i < routes.length(); i++) {
                    JSONObject route = routes.getJSONObject(i);
                    
                    if(!ignoredAgtuuids.contains(route.getString("agtuuid"))) {
                        this.routeRepository.touchRoute(
                            route.getString("agtuuid"), 
                            message.getString("agtuuid"), 
                            route.getInt("weight") + 1
                        );
                    }
                }
                
                responseBody = message.toString();
            } else if(type.equals("pull messages")) {
                responseBody = this.messageRepository.pullMessages(message.getString("isrc")).toString();
            } else if(type.equals("cascade request")) {
                String cscuuid = message.getString("cscuuid");
                
                if(this.cascadeRepository.touchCascade(cscuuid)) {
                    List<String> agtuuids = this.peerRepository.getAgtuuids();
                    
                    agtuuids.remove(message.getString("isrc"));
                    
                    for(int i = 0; i < agtuuids.size(); i++) {
                        message.put("dest", agtuuids.get(i));
                        
                        this.messageRepository.insert(new Message(agtuuids.get(i), message.toString()));
                    }
                    
                    message.put("dest", message.getString("isrc"));
                }
                
                responseBody = message.toString();
            }
        } else if(this.peerRepository.getAgtuuids().contains(message.getString("dest"))) {
            this.messageRepository.insert(new Message(message.getString("dest"), message.toString()));
            
            responseBody = message.toString();
        } else {
            String gtwuuid = this.routeRepository.getGtwuuid(message.getString("dest"));
            
            if(gtwuuid != null) {
                this.messageRepository.insert(new Message(gtwuuid, message.toString()));
            }
            
            responseBody = message.toString();
        }
        
        return responseBody;
    }
}