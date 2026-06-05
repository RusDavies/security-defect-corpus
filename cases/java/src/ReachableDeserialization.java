// JAVA-DESER-001 reachable unsafe deserialization fixture. DO NOT DEPLOY.
import java.io.ByteArrayInputStream;
import java.io.ObjectInputStream;

public class ReachableDeserialization {
    public Object readObjectFromRequest(byte[] requestBody) throws Exception {
        ObjectInputStream input = new ObjectInputStream(new ByteArrayInputStream(requestBody));
        return input.readObject();
    }
}
