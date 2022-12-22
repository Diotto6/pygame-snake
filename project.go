package main

import (
	"fmt"
	"log"
	"net/http"
	"encoding/json"
)

type dashboard struct {
	Title string `json:"title"`
	Rows []row `json:"rows"`
}

type row struct {
	Title string `json:"title"`
	Panels []panel `json:"panels"`
}

type panel struct {
	Type string `json:"type"`
	Title string `json:"title"`
	Datasource string `json:"datasource"`
	Targets []target `json:"targets"`
}

type target struct {
	RefId string `json:"refId"`
	Expr string `json:"expr"`
}

func main() {
	// create a new dashboard
	d := dashboard{
		Title: "My Dashboard",
		Rows: []row{
			row{
				Title: "Row 1",
				Panels: []panel{
					panel{
						Type: "graph",
						Title: "Graph Panel",
						Datasource: "prometheus",
						Targets: []target{
							target{
								RefId: "A",
								Expr: "sum(rate(http_requests_total[1m]))",
							},
						},
					},
				},
			},
		},
	}

	// create the dashboard in Grafana
	client := &http.Client{}
	req, err := http.NewRequest("POST", "http://localhost:3000/api/dashboards/db", nil)
	if err != nil {
		log.Fatal(err)
	}
	req.SetBasicAuth("admin", "admin")
	req.Header.Set("Content-Type", "application/json")
	b, err := json.Marshal(d)
	if err != nil {
		log.Fatal(err)
	}
	req.Body = nopCloser{bytes.NewReader(b)}
	res, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.StatusCode != 200 {
		log.Fatal("Failed to create dashboard")
	}
	fmt