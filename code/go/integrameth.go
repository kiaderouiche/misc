package main

import (
	"fmt"
	"math"
)

//function
func f(x float64) float64 {
	return 4.0 / (1 + (x-3)*(x-3))
}

//Method de rectangles
func Rectangles(a, b float64, n int) int{
	var S int = 0 //l'air du rectangle
	for i:=0; i < n; i++{
		xi := a+(b-a)*i/float64(n)
		xj := f((xi+xj)/2.0)*(xj-xi)
	}
	return S
}

//Methode de trapezes
func Trapezes() {

}

//Methode de simpson
func Simpson() {

}

func main() {

}
