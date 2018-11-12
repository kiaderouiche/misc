package main

// wrksrc="/usr/work"
// catypath="[a-z]*/[a-z]*"
// wrkspace="work/.packages/*.tgz"

// mkdir -p $HOME/pkgtmp

// Copy une method qui accepte des arguments ()
// for  sark in  $wrksrc/$catypath/$wrkspace
// do
// 	echo "Copy '$sark' to '$HOME/pkgtmp'"
// 	cp -f $sark $HOME/pkgtmp
// done

// exit 0

import "bufio"
import "fmt"
import "log"
import "os"
import "os/user"
import "path/filepath"

//import "regexp"

var pathwork string = "/usr/work"
var wrkspace = []string{"work", "packages", "tgz", "tbz"}

func CreatDst(namesdt string) string {
	use, err := user.Current()
	if err != nil {
		log.Fatal(err)
	}

	distd := filepath.Join(use.HomeDir, namesdt)
	os.MkdirAll(distd, 0711)
	if err != nil {
		log.Println("Error creating directory")
		log.Println(err)
	}

	return distd
}

func CopyPackage(dirdstName, dirsrcName string, pkgprefix string) error {

	ddst := CreatDst(dirdstName)
	fmt.Println(ddst)

	matched, err := filepath.Match(pkgprefix, fi.Name())
    if err != nil {
        fmt.Println(err) // malformed pattern
        return err       // this is fatal.
    }
    if matched {
        fmt.Println(fp)
    }

    return nil
}

func main() {
	dinput := bufio.NewReader(os.Stdin) //creation new dir
	fmt.Println("Please enter new name folder:")
	pkgtmp, err := dinput.ReadString('\n')

	if err != nil {
		fmt.Println("There were errors reading, exiting program.")
	}

	CopyPackage(pkgtmp, pathwork, wrkspace[2])
}
