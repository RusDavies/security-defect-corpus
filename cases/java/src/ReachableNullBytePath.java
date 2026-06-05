// JAVA-NULPATH-001 reachable null-byte/path validation fixture. DO NOT DEPLOY.
public class ReachableNullBytePath {
    public boolean isAllowedUpload(String filename) {
        return filename.endsWith(".png") || filename.endsWith(".jpg");
    }
}
