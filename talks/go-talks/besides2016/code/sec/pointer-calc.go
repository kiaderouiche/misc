package main

func main() {

	var ptrA *int
	var arr1 = [...]int{12, 23, 34, 45, 56, 67, 78, 89, 90}

	ptrA = &arr1 
	*ptrA = &arr1[1] 
	//fmt.Println(ptrA++) (invalid operation: ptrA++ (non-numeric type *int)
	ptrA = ptrA + 1 
}
