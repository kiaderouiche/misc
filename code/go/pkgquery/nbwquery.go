package main

/*
* K.I.A.Derouiche
* http://search.pkgsrc.se/
* simple pkgsrc / wip search script using pkgsrc.netbsd.se
* https://tutorialedge.net/golang/makefiles-for-go-developers/
 */

import (
	"fmt"
	"log"
	"os"

	"github.com/micro/cli"
)

var (
	__name__      = "nbwquery"
	__author__    = "K.I.A.Derouiche"
	__email__     = "kamel.derouiche@gmail.com"
	__copyright__ = "(c) 2019 K.I.A.Derouiche"
	__usage__     = "Get informations about a NetBSD package from pkgsrc.se"
	__urlweb__    = "http://search.pkgsrc.se/"
	__version__   = "1.0"
)

func main() {
	app := cli.NewApp()
	app.Name = __name__
	app.Authors = []cli.Author{
		{
			Name:  __author__,
			Email: __email__,
		},
	}
	app.Usage = __usage__

	app.Commands = []cli.Command{
		{
			Name:  "show",
			Usage: "Verbose package",
			Action: func(c *cli.Context) error {
				name := "pkgname"
				if c.NArg() > 0 {
					name = c.Args()[0]
					fmt.Println("Error de pkgname")
				}
				if name == "pkgse" {
					fmt.Println("pkgse")
				} else {
					fmt.Println("noname")
				}
				return nil
			},
		},
		{
			Name:  "stat",
			Usage: "numberic",
			Action: func(c *cli.Context) error {
				fmt.Println("")
				return nil
			},
		},
		{
			Name:  "version",
			Usage: "display information from tools",
			Action: func(c *cli.Context) error {
				fmt.Println("nbwquery version", __version__)
				return nil
			},
		},
	}

	err := app.Run(os.Args)
	if err != nil {
		log.Fatal(err)
		os.Exit(1)
	}
	os.Exit(0)
}
