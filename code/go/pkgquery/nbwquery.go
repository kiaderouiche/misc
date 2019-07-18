package main

/*
* K.I.A.Derouiche
* simple pkgsrc / wip search script using pkgsrc.netbsd.se
* https://tutorialedge.net/golang/makefiles-for-go-developers/
 */

import (
	"fmt"
	"os"

	"github.com/micro/cli"
)

var (
	name      = "nbwquery"
	author    = "K.I.A.Derouiche"
	email     = "kamel.derouiche@gmail.com"
	copyright = "(c) 2019 K.I.A.Derouiche"
	usage     = "Get informations about a NetBSD package from pkgsrc.se"
	urlweb    = "http://search.pkgsrc.se/"
	version   = "1.0"
)

func main() {
	app := cli.NewApp()

	fmt.Println(version)

	app.Run(os.Args)
}
