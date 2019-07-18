package main

/*
* K.I.A.Derouiche
* simple pkgsrc / wip search script using pkgsrc.netbsd.se
* https://tutorialedge.net/golang/makefiles-for-go-developers/
 */

import (
	"fmt"

	"github.com/micro/cli"
)

const version = "1.0"
const urlweb = "http://search.pkgsrc.se/"

func main() {

	app := cli.NewApp()

	app.Commands = [].cli.Command{
		{
			Name: "",

		},

	},
	fmt.Println(version)
}
