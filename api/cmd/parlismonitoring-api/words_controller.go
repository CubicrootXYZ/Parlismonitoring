package main

import (
    "encoding/json"
    "net/http"
    "log"
    m "./models"
)

func GetWordsUsage(w http.ResponseWriter, r *http.Request) {
    log.Print("GetWordUsage() called")
    w.Header().Set("Content-Type", "application/json")  // always return JSON
    var response m.Response
    vals := make([]interface{}, 0)
    hist := make(map[string]int)
    sql_base := "SELECT SUM(fk.word_count), file.publish_date FROM keyword INNER JOIN filekeyword as fk ON keyword.id = fk.keyword_id INNER JOIN file ON fk.file_id = file.id WHERE "
    sql_base2 := "SELECT SUM(fkc.word_count), file.publish_date FROM keyword INNER JOIN filekeywordcontent as fkc ON keyword.id = fkc.keyword_id INNER JOIN file ON fkc.file_id = file.id WHERE "

    // get database
    db, err := getDatabase()
    defer db.Close()
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #1")
        return
    }

    if r.FormValue("word") == "" {
        log.Print("No word provided")
        ErrorHandler(w, r, 422, "Property \"word\" not provided")
        return
    }

    words := CsvToList(r.FormValue("word"))
    sql := "keyword.word IN (?"

    if len(words) < 1 {
        log.Print("No word provided")
        ErrorHandler(w, r, 422, "Property \"word\" empty")
        return
    }

    for i, word := range words {
        vals = append(vals, word)

        if i < len(words)-1 {
            sql += ",?"
        }
    }
    sql += ") GROUP BY file.publish_date"
    log.Print(sql)

    // title words
    statement, err := db.Prepare(sql_base + sql)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 422, "Invalid statement #1")
        return
    }
    rows, err := statement.Query(vals...)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #2")
        return
    }

    for rows.Next() {
        var count int
        var date m.NTime
        err := rows.Scan(&count, &date)

        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #3")
            return
        }

        if date.Valid {
            hist[date.Time.Format(layoutISO)] = count
        }
    }

    // content words
    statement, err = db.Prepare(sql_base2 + sql)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 422, "Invalid statement #2")
        return
    }
    rows, err = statement.Query(vals...)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #4")
        return
    }

    for rows.Next() {
        var count int
        var date m.NTime
        err := rows.Scan(&count, &date)

        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #5")
            return
        }

        if date.Valid {
            t := date.Time.Format(layoutISO)

            if _, ok := hist[t]; ok {
                hist[t] += count
            } else {
                hist[t] = count
            }
        }
    }

    response.Data = hist
    response.Status = "success"
    json.NewEncoder(w).Encode(response)
}

func GetWords(w http.ResponseWriter, r *http.Request) {
    log.Print("GetWords() called")
    w.Header().Set("Content-Type", "application/json")  // always return JSON
    var response m.Response
    vals := make([]interface{}, 0)
    types := make([]string, 0)
    sql := "SELECT DISTINCT type FROM keyword WHERE "    // get database
    db, err := getDatabase()
    defer db.Close()
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #1")
        return
    }

    if r.FormValue("word") == "" {
        log.Print("No word provided")
        ErrorHandler(w, r, 422, "Property \"word\" not provided")
        return
    }

    words := CsvToList(r.FormValue("word"))
    sql += "keyword.word IN (?"

    if len(words) < 1 {
        log.Print("No word provided")
        ErrorHandler(w, r, 422, "Property \"word\" empty")
        return
    }

    for i, word := range words {
        vals = append(vals, word)

        if i < len(words)-1 {
            sql += ",?"
        }
    }
    sql += ")"
    log.Print(sql)

    statement, err := db.Prepare(sql)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 422, "Invalid statement #1")
        return
    }
    rows, err := statement.Query(vals...)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #2")
        return
    }

    for rows.Next() {
        var type_ string
        err := rows.Scan(&type_)

        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #3")
            return
        }

        types = append(types, type_)
    }

    response.Data = types
    response.Status = "success"
    json.NewEncoder(w).Encode(response)
}

