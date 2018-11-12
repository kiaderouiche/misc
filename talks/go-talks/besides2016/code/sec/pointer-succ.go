package main

import "fmt"

func main(){

	var ptrA, ptrB *int
	var arr1 = [...]int{12, 23, 34, 45, 56, 67, 78, 89, 90}

	ptrA = &arr1[2]
	ptrB = &arr1[5]
	fmt.Println("Addition: ", *ptrA + *ptrB)
	fmt.Println("Soustraction: ", *ptrA - *ptrB)
	fmt.Println("Multi: ", *ptrA * *ptrB)
	fmt.Println(*ptrA+2, *ptrB-8)
}