
package main

/*
* K.I.A.Derouiche
* simple pkgsrc / wip search script using pkgsrc.netbsd.se
* https://tutorialedge.net/golang/makefiles-for-go-developers/
*/

import (
  "fmt"
  
  "github.com/urfave/cli"
)

const version = "1.0"
const urlweb = "http://search.pkgsrc.se/"

func main(){
  fmt.Println(version)
}
