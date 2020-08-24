package main

import (
	"fmt"
	"math"
	//"math/big"
)

// Richard Brent and Eugene Salamin algorithm (version 1.0)
// a0 = 1/2; b0 = 1/sqrt(2); so = 1/2
// a_{n+1} = a_{n}+b_{n}/2
// b_{n+1} = sqrt(a_{n}*b_{n})
// c_{n+1} = a_{n+1}^{2} - b_{n+1}^{2}
// s_{n+1} = s_{n}-2^{n+1}*c_{n+1}
// Reference:
// https://www-fourier.ujf-grenoble.fr/~demailly/manuscripts/pi_ellipt.pdf
// PI= 3.141593

const prec = 10

func brentSala(n int) float64 {
	var d float64 = 2.0
	var a float64 = 1.0
	var u float64 = 0.5
	s := u
	var b float64 = s * math.Sqrt(d)
	c, k := a*a-b*b, 1.0
	for i := 0; i <= n; i++ {
		a, b = (a+b)*u, math.Sqrt((a * b))
		c, k = a*a-b*b, 2*k
		s = s - c*k
	}
	return d * a * a / s
}

func main() {
	fmt.Printf("L'approximation PI= %f\n", brentSala(15))
}
