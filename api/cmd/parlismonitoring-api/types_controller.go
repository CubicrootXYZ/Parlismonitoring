package main

import (
    "encoding/json"
    "net/http"
    "log"
    m "./models"
)

func GetTypes(w http.ResponseWriter, r *http.Request) {
    log.Print("GetTypes() called")
    w.Header().Set("Content-Type", "application/json")  // always return JSON
    var response m.Response
    types := make([]string, 0)

    // get database
    db, err := getDatabase()
    defer db.Close()
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #1")
        return
    }

    rows, err := db.Query("SELECT DISTINCT type FROM file")
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

        types = append(types, a)
    }

    response.Data = types
    response.Status = "success"
    json.NewEncoder(w).Encode(response)
}

func GetTypesStatistics(w http.ResponseWriter, r *http.Request) {
    log.Print("GetTypesStatistics() called")
    w.Header().Set("Content-Type", "application/json")  // always return JSON
    var response m.Response
    types_stats := make(map[string]*m.TypeStats)

    // get database
    db, err := getDatabase()
    defer db.Close()
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #1")
        return
    }

    rows, err := db.Query("SELECT type, COUNT(*), MAX(publish_date) FROM file GROUP BY type")
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #2")
        return
    }

    for rows.Next() {
        var a m.TypeStats
        err := rows.Scan(&a.Type, &a.Files, &a.LastPublish)
        if err != nil {
            log.Print(err.Error())
        }

        types_stats[a.Type] = &a
    }

    response.Data = types_stats
    response.Status = "success"
    json.NewEncoder(w).Encode(response)
}