package main

import (
	"fmt"
	"github.com/gonum/matrix/mat64"
	"math"
)

//This function transform spherical to cartesian coordinates
func spher2cartesian(v mat64.Vector) {
	// r := v[0]
	// teta := v[1] * math.Pi / 180.0
	// phi := v[2] * math.Pi / 180.0
	// x := r * math.Sin(teta) * math.Cos(phi)
	// y := r * math.Sin(teta) * math.Sin(phi)
	// z := r * math.Cos(teta)

	// fmt.Printf("%f %f %f\n", x, y, z)
}

func main() {
	m := mat64.Vector(3, []float64{
		1.2, 3.5, 8.6,
	})
	spher2cartesian(m)
}
