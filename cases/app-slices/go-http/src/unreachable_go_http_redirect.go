// APP-GOHTTP-REDIR-001 unreachable/safe paired fixture.
package main

import (
    "net/http"
    "strings"
)

func retiredRedirect(w http.ResponseWriter, r *http.Request) {
    http.Redirect(w, r, r.URL.Query().Get("next"), http.StatusFound)
}

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
