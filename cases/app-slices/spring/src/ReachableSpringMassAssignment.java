// APP-SPRING-MASSASSIGN-001 reachable vulnerable fixture. DO NOT DEPLOY.
@interface RestController {}
@interface PostMapping { String value(); }
@interface RequestBody {}

class ProfileRequest {
    public String displayName;
    public boolean isAdmin;
}

class UserProfile {
    public String displayName;
    public boolean isAdmin;
}

@RestController
public class ReachableSpringMassAssignment {
    @PostMapping("/profile")
    public UserProfile updateProfile(@RequestBody ProfileRequest request) {
        UserProfile profile = new UserProfile();
        profile.displayName = request.displayName;
        profile.isAdmin = request.isAdmin;
        return profile;
    }
}
