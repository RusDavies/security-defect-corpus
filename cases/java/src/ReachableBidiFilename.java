// JAVA-BIDI-001 reachable bidi-control filename deception fixture. DO NOT DEPLOY.
public class ReachableBidiFilename {
    public boolean isSafeDisplayName(String filename) {
        return !filename.contains("/") && !filename.contains("\\");
    }
}
