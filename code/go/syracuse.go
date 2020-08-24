package main

//
// Syracuse conjecture
// Please Update code
//

import (
	"fmt"
	// 	"math"
)

func Syracuse(u0, n int) int {
	u := u0
	for k := 1; k < n; k++ {
		if u%2 == 0 {
			u = u / 2
		} else {
			u = 3*u + 1
		}
	}

	return u
}

func main() {
	//Worng result
	fmt.Println(Syracuse(2, 0))

}
