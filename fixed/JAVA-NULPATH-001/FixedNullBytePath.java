// JAVA-NULPATH-001 fixed-version fixture for patch-diff evaluation.
import java.text.Normalizer;

public class FixedNullBytePath {
    public boolean isAllowedUpload(String filename) {
        if (filename.indexOf('\0') >= 0) return false;
        if (filename.matches(".*[\\p{Cntrl}].*")) return false;
        String normalized = Normalizer.normalize(filename, Normalizer.Form.NFC);
        return normalized.endsWith(".png") || normalized.endsWith(".jpg");
    }
}
