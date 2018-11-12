package main

type Point struct { x, y float64 }

func (p *Point) Norm() float64 { 
	return math.Sqrt(p.x*p.x + p.y*p.y)
}

/* Un type qui a une fonction d'écriture. Cela peut être un fichier,
une prise réseau, une chaîne de caractères, etc */

type NormInterface interface {
	Norm() float64
}

func computeNorm(x *NormInterface) float64 {
	return x.Norm()
}