// JAVA-METADATA-NET-001 reachable cloud metadata-service access fixture. DO NOT DEPLOY.
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;

public class ReachableMetadataServiceAccess {
    public HttpRequest buildRequest() {
        return HttpRequest.newBuilder()
            .uri(URI.create("http://169.254.169.254/latest/meta-data/iam/security-credentials/"))
            .GET()
            .build();
    }

    public void fetchMetadata() throws Exception {
        HttpClient.newHttpClient().send(buildRequest(), java.net.http.HttpResponse.BodyHandlers.ofString());
    }
}
