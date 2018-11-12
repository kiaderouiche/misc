package main

import "fmt"
import "math"

//import "math/big"

///
/// x^2 - x -1 = 0
/// x = 1+sqrt(5)/2
///
const PHI = 1.6180339887

func main() {
	var phi float64 = (1 + math.Sqrt(5)) / 2
	fmt.Printf("Golden Ratio(modern): phi = (1+sqrt(5))/2 = %f\n", phi)
	fmt.Printf("Golden Ratio(last): phi = [1+(phi+0.618)]/2 = %f\n",(1+(phi+0.618))/2)
	//fmt.Printf("(phi+1/phi)/2 = phi = %f\n", (phi+1/phi)/2)
	fmt.Printf("phi + 1 = phi**2 = %f\n", phi+1)
	fmt.Printf("phi-1 = 1+phi = %f\n", phi-1)

}
