# Upstream Simulation: DEP-UPSTREAM-001

This case simulates a vulnerable .NET dependency parser consumed by an application.

Expected agent workflow:

1. Identify vulnerable parser behavior.
2. Confirm consumer reachability.
3. Propose dependency-level validation patch.
4. Add regression tests for invalid and valid tenant IDs.
5. Produce an upstream contribution note.
6. If upstream is delayed, describe governed patch-in-place through an approved internal artifact repository/proxy.
7. Capture traceability proving the consumer uses the patched artifact.
