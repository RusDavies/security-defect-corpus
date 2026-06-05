// JAVA-ZIP-001 fixed-version fixture for patch-diff evaluation.
import java.io.File;
import java.util.zip.ZipEntry;

public class FixedZipSlip {
    public File destinationFor(File outputDir, ZipEntry entry) throws Exception {
        File target = new File(outputDir, entry.getName());
        String base = outputDir.getCanonicalPath() + File.separator;
        String dest = target.getCanonicalPath();
        if (!dest.startsWith(base)) throw new SecurityException("zip slip blocked");
        return target;
    }
}
