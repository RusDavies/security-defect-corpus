// APP-GOHTTP-REDIR-001 fixed-version fixture for patch-diff evaluation.
package main

import (
    "net/http"
    "strings"
)

func localRedirectTarget(next string) (string, bool) {
    if !strings.HasPrefix(next, "/") || strings.HasPrefix(next, "//") {
        return "", false
    }
    return next, true
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
    next, ok := localRedirectTarget(r.URL.Query().Get("next"))
    if !ok {
        http.Error(w, "invalid redirect", http.StatusBadRequest)
        return
    }
    http.Redirect(w, r, next, http.StatusFound)
}
