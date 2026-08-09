// GO-PROXY-BYPASS-001 fixed-version fixture for patch-diff evaluation.
package main

import "net/http"

func FetchUpdate(client *http.Client, url string) (*http.Response, error) {
    return client.Get(url)
}
