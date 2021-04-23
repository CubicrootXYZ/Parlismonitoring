package models

type AuthorStats struct {
    Author      string `json:"author"`
    Files       NInt    `json:"files"`
    LastPublish NTime   `json:"last_publish_date"`
}