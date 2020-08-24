package main

import (
	"fmt"
	"time"
)

func saycall(n int) {
	for i := 0; i < 5; i++ {
		time.Sleep(100 * time.Millisecond)
		fmt.Printf("%d\n", n)
	}
}

func main() {
	go saycall(1)
	saycall(0)
}
