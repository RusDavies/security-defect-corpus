// GO-DNS-EXFIL-001 safe paired fixture.
package main

func ReportBuild() string {
    return "build metadata recorded locally"
}

func main() {
    _ = ReportBuild()
}
