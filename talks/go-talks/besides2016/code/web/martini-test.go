package main

import ("net/http"
    "github.com/go-martini/martini"
    "github.com/martini-contrib/gzip"
    "github.com/martini-contrib/render")

func main() {
  m := martini.Classic()
  m.Use(gzip.All())
  m.Use(render.Renderer())
  m.Get("/", func() string {
    return "Hello world!"
  })
  m.Get("/hello/:name", func(req *http.Request,
                             params martini.Params,
                             r render.Render) {
    data := map[string]interface{}{"name": params["name"]}
    typ := "html"
    if query := req.URL.Query()["type"]; len(query) > 0 {
      typ = query[0]
    }
    switch typ {
    case "json": r.JSON(200, data)
    default: r.HTML(200, "hello", data)
    }
  })
  m.Run()