// Superficial JAVA-DESER-001 repair: checks payload size but still deserializes untrusted object streams.
import java.io.ByteArrayInputStream;
import java.io.ObjectInputStream;

public class ReachableDeserialization {
    public Object readObjectFromRequest(byte[] requestBody) throws Exception {
        if (requestBody.length > 4096) {
            throw new IllegalArgumentException("payload too large");
        }
        ObjectInputStream input = new ObjectInputStream(new ByteArrayInputStream(requestBody));
        return input.readObject();
    }
}
