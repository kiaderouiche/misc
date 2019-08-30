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

import (
	"fmt"
	"os"

	"github.com/micro/cli"
)

var ()

//Function to compress PDF via Ghostscript command line interface
func compress(inputFilePath string, outputFilePath string, power int) {
	power = 0

	//quality := map[int]string{
	//	0: "/default",
	//	1: "/prepress",
	//	2: "/printer",
	//	3: "/ebook",
	//	4: "/screen",
	//}

	//Temp code!
	fmt.Println("Compress PDF...")

}

func main() {
	app := cli.NewApp()

	app.Flags = []cli.Flag{
		cli.StringFlag{
			Name:  "input",
			Usage: "Relative or absolute path of the input `PDF file`",
		},
		cli.StringFlag{
			Name:  "output, out",
			Usage: "Relative or absolute path of the output `PDF file`",
		},
		cli.StringFlag{
			Name:  "compress, c",
			Usage: "Compression level from `[0-4]`",
		},
		cli.StringFlag{
			Name:  "backup, b",
			Usage: "Backup the old `PDF file`",
		},
	}

	app.Run(os.Args)

}
