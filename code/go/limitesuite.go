package main

import (
	"fmt"
	"math"
)

var u float64 = 1

func main() {
	for i := 0; i <= 1; i++ {
		u = math.Sqrt(1 + u)
	}
	fmt.Println(u)
}
