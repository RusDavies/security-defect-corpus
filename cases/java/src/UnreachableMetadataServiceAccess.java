// JAVA-METADATA-NET-001 safe paired fixture.
import java.net.URI;

public class UnreachableMetadataServiceAccess {
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
