func(peugeot chan string, renault chan string) {
  select {
       case order, status := <- peugeot:
         ...
       case order, status := <- renault:
         ...
  }
}