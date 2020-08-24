package main

import "fmt"

func echo(ch chan string) {
	n := <-ch // stocker dans v une donnée reçue du channel
	fmt.Printf("Received %d\n", n)
	ch <- n  // envoyer 1 dans le channel
}

func main() {
	ch := make(chan string)
	go echo(ch)
	ch <- "hello handsome !"
	<-ch // recevoir une valeur du channel et la jeter
}
