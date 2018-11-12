package main

type list struct {
    buf  [10]byte
    next *list
}

func main() {
    var l *list
    for {
        l = &list{next: l}
    }
}