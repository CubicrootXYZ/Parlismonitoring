package models

type TypeStats struct {
    Type        string `json:"type"`
    Files       NInt    `json:"files"`
    LastPublish NTime   `json:"last_publish_date"`
}