// JAVA-ZIP-001 reachable unsafe archive extraction fixture. DO NOT DEPLOY.
import java.io.File;
import java.util.zip.ZipEntry;

public class ReachableZipSlip {
    public File destinationFor(File outputDir, ZipEntry entry) {
        return new File(outputDir, entry.getName());
    }
}
