package main

import "fmt"

func main(){
	
	data := map[string]string{
		"foo": "bar",
		"hello": "world",
	}
	
	for k, v := range data{
		fmt.Printf("%s -> %s\n", k, v)
	}
}