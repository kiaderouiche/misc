package main

func main() {
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("Une erreur dans ce package: %v", r)
		}
	}()
	var do_word []string
	panicstat(do_word)
}
