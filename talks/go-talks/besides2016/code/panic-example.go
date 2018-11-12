package main

import "fmt"

func panicstat(word []string) int {

	defer func() {

		fmt.Println("Clean code")
	}()

	if len(word) == 0 {
		panic("no word!")
	}

	return len(word)
}

func main() {
	var do_word []string
	panicstat(do_word)
}
