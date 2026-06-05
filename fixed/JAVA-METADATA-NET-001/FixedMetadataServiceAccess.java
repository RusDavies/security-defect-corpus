// JAVA-METADATA-NET-001 fixed-version fixture for patch-diff evaluation.
import java.net.URI;

public class FixedMetadataServiceAccess {
    public URI validatedEndpoint(String configuredEndpoint) {
        URI endpoint = URI.create(configuredEndpoint);
        if (endpoint.getHost() == null || endpoint.getHost().equals("169.254.169.254")) {
            throw new SecurityException("metadata-service endpoint blocked");
        }
        if (!endpoint.getScheme().equals("https")) {
            throw new SecurityException("https required");
        }
        return endpoint;
    }
}
