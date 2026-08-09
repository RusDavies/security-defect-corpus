// JAVA-LDAP-001 fixed-version fixture for patch-diff evaluation.
import javax.naming.directory.DirContext;
import javax.naming.directory.SearchControls;

public class FixedLdapInjection {
    private final DirContext directory;
    public FixedLdapInjection(DirContext directory) { this.directory = directory; }

    private String escapeLdapFilter(String value) {
        return value.replace("\\", "\\5c").replace("*", "\\2a").replace("(", "\\28").replace(")", "\\29");
    }

    public Object findUser(String username) throws Exception {
        String escaped = escapeLdapFilter(username);
        return directory.search("ou=people,dc=example,dc=test", "(&(objectClass=user)(uid=" + escaped + "))", new SearchControls());
    }
}
