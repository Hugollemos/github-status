package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

type GitHubStatus struct {
	Page struct {
		ID        string    `json:"id"`
		Name      string    `json:"name"`
		URL       string    `json:"url"`
		TimeZone  string    `json:"time_zone"`
		UpdatedAt time.Time `json:"updated_at"`
	} `json:"page"`
	Status struct {
		Indicator   string `json:"indicator"`
		Description string `json:"description"`
	} `json:"status"`
}

func checkGitHubStatus() (*GitHubStatus, error) {
	resp, err := http.Get("https://www.githubstatus.com/api/v2/summary.json")
	if err != nil {
		return nil, fmt.Errorf("error fetching GitHub status: %v", err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("error reading response body: %v", err)
	}

	var status GitHubStatus
	if err := json.Unmarshal(body, &status); err != nil {
		return nil, fmt.Errorf("error parsing JSON: %v", err)
	}

	return &status, nil
}

func main() {
	log.Println("GitHub Status Monitor Bot Started")
	
	for {
		status, err := checkGitHubStatus()
		if err != nil {
			log.Printf("Error: %v\n", err)
			time.Sleep(5 * time.Minute)
			continue
		}

		log.Printf("GitHub Status: %s - %s\n", status.Status.Indicator, status.Status.Description)
		log.Printf("Last Updated: %s\n", status.Page.UpdatedAt)

		time.Sleep(5 * time.Minute)
	}
} 