package main

// Author: K.I.A.Derouiche
// MIT license

/*
 * Simple Golang wrapper script to use ghostscript function to
 * compress PDF files.
 *
 * Compression levels:
 *
 * 0: default
 * 1: prepress
 * 2: printer
 * 3: ebook
 * 4: screen
 *
 *
 * Dependency: Ghostscript
 */

import "fmt"
import "github.com/micro/cli"

//Function to compress PDF via Ghostscript command line interface
func compress(inputFilePath string, outputFilePath string, power int) {
	power = 0

	quality := map[int]string{
		0: "/default",
		1: "/prepress",
		2: "/printer",
		3: "/ebook",
		4: "/screen",
	}

	//Temp code!
	fmt.Println("Compress PDF...")

}

func main() {
	app := cli.NewApp()
	app.Name = "go-pdf_compressor"
	app.Usage = ""
	fmt.Println("Welcome to pdf-compressor")
}
