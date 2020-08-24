package main

//1.0 version

import "fmt"

func addA(tic int) {
	fmt.Println("tic: First Func", tic+1)
}


func addB(toc int) {
	fmt.Println("toc: Next Func", toc-1)
}

func main(){
	defer addA(1)
	addB(-2)	
}