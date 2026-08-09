// GO-TEMPLATE-XSS-001 unreachable/safe paired fixture.
package main

import (
    "bytes"
    htmltemplate "html/template"
    "text/template"
)

func retiredRenderComment(author string) string {
    tmpl := template.Must(template.New("comment").Parse("<p>" + author + "</p>"))
    var out bytes.Buffer
    tmpl.Execute(&out, nil)
    return out.String()
}

func RenderComment(author string) string {
    tmpl := htmltemplate.Must(htmltemplate.New("comment").Parse("<p>{{.Author}}</p>"))
    var out bytes.Buffer
    tmpl.Execute(&out, map[string]string{"Author": author})
    return out.String()
}
