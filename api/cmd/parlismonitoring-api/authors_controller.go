package main

import (
    "encoding/json"
    "net/http"
    "log"
    m "./models"
)

func GetAuthors(w http.ResponseWriter, r *http.Request) {
    log.Print("GetAuthors() called")
    w.Header().Set("Content-Type", "application/json")  // always return JSON
    var response m.Response
    authors := make([]string, 0)

    // get database
    db, err := getDatabase()
    defer db.Close()
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #1")
        return
    }

    rows, err := db.Query("SELECT DISTINCT author FROM file")
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #2")
        return
    }

    for rows.Next() {
        var a string
        err := rows.Scan(&a)

        if err != nil {
            log.Print(err.Error())
        }

        authors = append(authors, a)
    }

    response.Data = authors
    response.Status = "success"
    json.NewEncoder(w).Encode(response)
}

func GetAuthorsStatistics(w http.ResponseWriter, r *http.Request) {
    log.Print("GetAuthorsStatistics() called")
    w.Header().Set("Content-Type", "application/json")  // always return JSON
    var response m.Response
    authors_stats := make(map[string]*m.AuthorStats)

    // get database
    db, err := getDatabase()
    defer db.Close()
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #1")
        return
    }

    rows, err := db.Query("SELECT author, COUNT(*), MAX(publish_date) FROM file GROUP BY author")
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #2")
        return
    }

    for rows.Next() {
        var a m.AuthorStats
        err := rows.Scan(&a.Author, &a.Files, &a.LastPublish)

        if err != nil {
            log.Print(err.Error())
        }

        authors_stats[a.Author] = &a
    }

    response.Data = authors_stats
    response.Status = "success"
    json.NewEncoder(w).Encode(response)
}