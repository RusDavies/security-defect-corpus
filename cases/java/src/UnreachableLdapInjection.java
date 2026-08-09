// JAVA-LDAP-001 unreachable/safe paired fixture.
import javax.naming.directory.DirContext;
import javax.naming.directory.SearchControls;

public class UnreachableLdapInjection {
    private final DirContext directory;
    public UnreachableLdapInjection(DirContext directory) { this.directory = directory; }

    private Object retiredFindUser(String username) throws Exception {
        String filter = "(&(objectClass=user)(uid=" + username + "))";
        return directory.search("ou=people,dc=example,dc=test", filter, new SearchControls());
    }

    public Object findUser(String username) throws Exception {
        String escaped = username.replace("\\", "\\5c").replace("*", "\\2a").replace("(", "\\28").replace(")", "\\29");
        return directory.search("ou=people,dc=example,dc=test", "(&(objectClass=user)(uid=" + escaped + "))", new SearchControls());
    }
}
