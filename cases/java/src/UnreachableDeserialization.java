// JAVA-DESER-001 safe/unreachable paired fixture.
import java.io.ByteArrayInputStream;
import java.io.ObjectInputFilter;
import java.io.ObjectInputStream;

public class UnreachableDeserialization {
    private Object legacyUnsafeRead(byte[] data) throws Exception {
        return new ObjectInputStream(new ByteArrayInputStream(data)).readObject();
    }

    public Object readObjectFromTrustedCache(byte[] data) throws Exception {
        ObjectInputStream input = new ObjectInputStream(new ByteArrayInputStream(data));
        input.setObjectInputFilter(ObjectInputFilter.Config.createFilter("java.lang.String;!*"));
        return input.readObject();
    }
}
