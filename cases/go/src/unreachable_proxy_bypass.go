// GO-PROXY-BYPASS-001 unreachable/safe pair fixture. DO NOT DEPLOY.
package main

import (
    "net/http"
    "time"
)

func retiredDirectClient() *http.Client {
    return &http.Client{Transport: &http.Transport{Proxy: nil}, Timeout: 2 * time.Second}
}

func FetchUpdate(client *http.Client, url string) (*http.Response, error) {
    return client.Get(url)
}
