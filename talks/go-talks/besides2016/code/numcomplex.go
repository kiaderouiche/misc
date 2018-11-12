package main

import "fmt"

func somme(a []float64) {

	var total float64 = 0;

	for _, v:= range a{
		total += v;
	}
	fmt.Println(total);
}

func main(){

	s := make([]float64, 5, 5);
	s =[]float64{1.3, 6.9, -8.23, -9.1452, -69.20};

	somme(s);

}