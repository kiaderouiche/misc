package main

import "fmt"
import "math"

func main() {

	var entropy float64 = 0.0
	var proba int = 0
	var probas = make([]float64, 8)
	probas = []float64{0.090909091, 0.090909091, 0.272727273, 0.181818182, 0.090909091, 0.090909091, 0.090909091, 0.090909091}

	for proba < len(probas) {

		entropy -= probas[proba] * math.Log2(probas[proba])
		proba++
	}

	fmt.Printf("[Hello World] Entropique: %f\n", entropy)
}
