// APP-SPRING-MASSASSIGN-001 unreachable/safe paired fixture.
@interface RestController {}
@interface PostMapping { String value(); }
@interface RequestBody {}

class SafeProfileRequest {
    public String displayName;
    public boolean isAdmin;
}

class SafeUserProfile {
    public String displayName;
    public boolean isAdmin;
}

@RestController
public class UnreachableSpringMassAssignment {
    private SafeUserProfile retiredBindAllFields(SafeProfileRequest request) {
        SafeUserProfile profile = new SafeUserProfile();
        profile.displayName = request.displayName;
        profile.isAdmin = request.isAdmin;
        return profile;
    }

    @PostMapping("/profile")
    public SafeUserProfile updateProfile(@RequestBody SafeProfileRequest request) {
        SafeUserProfile profile = new SafeUserProfile();
        profile.displayName = request.displayName;
        profile.isAdmin = false;
        return profile;
    }
}
