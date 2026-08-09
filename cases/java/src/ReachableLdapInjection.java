// JAVA-LDAP-001 reachable vulnerable fixture. DO NOT DEPLOY.
import javax.naming.directory.DirContext;
import javax.naming.directory.SearchControls;

public class ReachableLdapInjection {
    private final DirContext directory;
    public ReachableLdapInjection(DirContext directory) { this.directory = directory; }

    public Object findUser(String username) throws Exception {
        String filter = "(&(objectClass=user)(uid=" + username + "))";
        return directory.search("ou=people,dc=example,dc=test", filter, new SearchControls());
    }
}
