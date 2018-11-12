package main

//mistakes code!

func Pgcd(a, b int) int {
	x, y = a, b
	for y > 0 {
		//[q, r] = div(x, y)
		if r == 0 {
			pgcd := y
			y = 0
		} else {
			//[q1, r1] = div(y, r)
			x = r
			pgcd = x
			y = r1
		}

	}

}

func main() {
	Pgcd(a, b)
}
