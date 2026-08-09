// GO-TEMPLATE-XSS-001 fixed-version fixture for patch-diff evaluation.
package main

import (
    "bytes"
    "html/template"
)

func RenderComment(author string) string {
    tmpl := template.Must(template.New("comment").Parse("<p>{{.Author}}</p>"))
    var out bytes.Buffer
    tmpl.Execute(&out, map[string]string{"Author": author})
    return out.String()
}
