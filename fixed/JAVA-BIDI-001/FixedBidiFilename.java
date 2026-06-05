// JAVA-BIDI-001 fixed-version fixture for patch-diff evaluation.
public class FixedBidiFilename {
    public boolean isSafeDisplayName(String filename) {
        if (filename.matches(".*[\\u202A-\\u202E\\u2066-\\u2069].*")) return false;
        return !filename.contains("/") && !filename.contains("\\");
    }
}
