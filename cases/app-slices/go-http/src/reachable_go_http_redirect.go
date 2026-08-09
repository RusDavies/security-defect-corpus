// APP-GOHTTP-REDIR-001 reachable vulnerable fixture. DO NOT DEPLOY.
package main

import "net/http"

func loginHandler(w http.ResponseWriter, r *http.Request) {
    next := r.URL.Query().Get("next")
    http.Redirect(w, r, next, http.StatusFound)
}
