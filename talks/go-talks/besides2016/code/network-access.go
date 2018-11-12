package main

func main(){
	
	res, err := http.Get("http://api.openweathermap.org/data/2.5/weather?q=Portland")
	if err != nil{
		log.Fatal(err);
	}
	defer res.Body.Close();

	var w struct{
		weather [] struct{
			Desc string `json: "description"`
			} `json: "weather"`
		}
	}

	if err = json.NewDecoder(res.Body).Decode(&w) {
		log.Fatal(err)
	}
	fmt.Printf("No need to rush outside, we have %v.", weather[0].Desc);
}