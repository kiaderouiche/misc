package main 

import "fmt"

func main(){
	
	var array [10]int
	var sArray []int
	// Déterminée à partir du nombre de valeurs initiales
	list := [...]string{"a", "b", "c", "d", "e", "f"}
	other :=append(list[0:2], list[3:5]...)
	for k, v := range other{
		fmt.Printf("%d -> %s\n", k, v)
	}
}