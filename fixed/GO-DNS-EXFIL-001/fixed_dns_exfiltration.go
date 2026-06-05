// GO-DNS-EXFIL-001 fixed-version fixture for patch-diff evaluation.
package main

func ReportBuild() string {
    return "build metadata recorded locally"
}

func main() {
    _ = ReportBuild()
}
