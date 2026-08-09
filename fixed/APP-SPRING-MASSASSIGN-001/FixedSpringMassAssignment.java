// APP-SPRING-MASSASSIGN-001 fixed-version fixture for patch-diff evaluation.
@interface RestController {}
@interface PostMapping { String value(); }
@interface RequestBody {}

class FixedProfileRequest {
    public String displayName;
    public boolean isAdmin;
}

class FixedUserProfile {
    public String displayName;
    public boolean isAdmin;
}

@RestController
public class FixedSpringMassAssignment {
    @PostMapping("/profile")
    public FixedUserProfile updateProfile(@RequestBody FixedProfileRequest request) {
        FixedUserProfile profile = new FixedUserProfile();
        profile.displayName = request.displayName;
        profile.isAdmin = false;
        return profile;
    }
}
