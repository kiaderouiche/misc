package main

import "os"
import "log"

func main() {
	err := os.RemoveAll("/mnt")
	if err != nil {
		log.Fatal(err)
	}
}
