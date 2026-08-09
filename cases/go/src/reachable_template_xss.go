// GO-TEMPLATE-XSS-001 reachable vulnerable fixture. DO NOT DEPLOY.
package main

import (
    "bytes"
    "text/template"
)

func RenderComment(author string) string {
    tmpl := template.Must(template.New("comment").Parse("<p>" + author + "</p>"))
    var out bytes.Buffer
    tmpl.Execute(&out, nil)
    return out.String()
}
