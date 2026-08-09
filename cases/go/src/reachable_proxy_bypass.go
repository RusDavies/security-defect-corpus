// GO-PROXY-BYPASS-001 reachable proxy-bypass fixture. DO NOT DEPLOY.
package main

import (
    "net/http"
    "time"
)

func FetchUpdate() (*http.Response, error) {
    client := &http.Client{
        Transport: &http.Transport{Proxy: nil},
        Timeout:   2 * time.Second,
    }
    return client.Get("https://updates.example.invalid/check")
}
