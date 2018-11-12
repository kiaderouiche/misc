package main

import "net/http"

func HelloWorld(w http.ResponseWriter, req *http.Request) {
    w.Write([]byte("Hello world!"))
}

func main() {
    http.HandleFunc("/", HelloWorld)
    http.ListenAndServe("127.0.0.1:8000", nil)
}