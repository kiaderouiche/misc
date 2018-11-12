package main

import (
	"fmt"
	"github.com/gonum/matrix/mat64"
)

func main() {
	dx := make([]float64, 3)
	//
	dx[0] = 2
	dx[1] = 2
	dx[2] = 3
	//
	x := mat64.NewDense(3, 1, dx)

	y := mat64.NewDense(3, 1, []float64{
		1, 4, 5,
	})
	z := mat64.NewDense(3, 1, []float64{
		0, 0, 0,
	})
	z.Add(x, y)

	fmt.Printf("%f %f %f\n", z.At(0, 0), z.At(0, 0), z.At(1, 0), z.At(2, 0))

}
