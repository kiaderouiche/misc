package main

import "bufio"
import "fmt"
import "math"
import "os"

func main() {

	var linec int
	// Open the file.
	f, _ := os.Open("/etc/fstab")
	// Create a new Scanner for the file.
	scanner := bufio.NewScanner(f)
	// Loop over all lines in the file and print them.
	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println(line)
	}
}
