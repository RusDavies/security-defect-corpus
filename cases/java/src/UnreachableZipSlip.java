// JAVA-ZIP-001 safe paired fixture.
import java.io.File;
import java.util.zip.ZipEntry;

public class UnreachableZipSlip {
    public File destinationFor(File outputDir, ZipEntry entry) throws Exception {
        File target = new File(outputDir, entry.getName());
        String base = outputDir.getCanonicalPath() + File.separator;
        String dest = target.getCanonicalPath();
        if (!dest.startsWith(base)) throw new SecurityException("zip slip blocked");
        return target;
    }
}
