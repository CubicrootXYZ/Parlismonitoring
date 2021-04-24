package main

import (
    "encoding/json"
    "net/http"
    "strings"
    "time"
    "log"
    m "./models"
    "strconv"
    "math"
)

const (
    layoutISO = "2006-01-02"
    layoutUS  = "January 2, 2006"
)

func FilesSearch(w http.ResponseWriter, r *http.Request) {
    log.Print("FilesSearch() called")
    w.Header().Set("Content-Type", "application/json")  // always return JSON

    // get database
    db, err := getDatabase()
    defer db.Close()
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #1")
        return
    }

    // setup variables for later
    conds := make([]string, 0)
    vals := make([]interface{}, 0)
    files := make([]m.File, 0)
    var response m.Response
    var pagination m.Pagination
    pagination.Page = 1
    pagination.Items = 50

    // read parameters from request
    page_ := r.FormValue("page")
    if page_ != "" {
        page, err := strconv.Atoi(page_)
        if err == nil {
            pagination.Page = page
        }
    }

    start_ := r.FormValue("start")
    if start_ != "" {
        start, err := time.Parse(layoutISO, start_)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 422, "Can not read \"start\"")
            return
        }
        conds = append(conds, "file.publish_date >= ?")
        vals = append(vals, start.Format("2006-01-02"))
    } else {
        conds = append(conds, "file.publish_date >= ?")
        vals = append(vals, "DATE_SUB(NOW(), INTERVAL 182 DAY)")
    }

    end_ := r.FormValue("end")
    if end_ != "" {
        end, err := time.Parse(layoutISO, end_)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 422, "Can not read \"end\"")
            return
        }
        conds = append(conds, "file.publish_date <= ?")
        vals = append(vals, end.Format("2006-01-02"))
    }

    if r.FormValue("title") != "" {
        title_values := CsvToList(r.FormValue("title"))
        conds = append(conds, "fkk.word in (?" + strings.Repeat(", ?", len(title_values)-1) + ")")
        for _, title_value := range title_values {
            vals = append(vals, title_value)
        }

    }

    if r.FormValue("content") != "" {
        content_values := CsvToList(r.FormValue("content"))
        conds = append(conds, "fkck.word in (?" + strings.Repeat(", ?", len(content_values)-1) + ")")
        for _, content_value := range content_values {
            vals = append(vals, content_value)
        }
    }

    if r.FormValue("author") != "" {
        author_values := CsvToList(r.FormValue("author"))
        conds = append(conds, "file.author in (?" + strings.Repeat(", ?", len(author_values)-1) + ")")
        for _, author_value := range author_values {
            vals = append(vals, author_value)
        }
    }
    
    if r.FormValue("type") != "" {
        type_values := CsvToList(r.FormValue("type"))
        conds = append(conds, "file.type in (?" + strings.Repeat(", ?", len(type_values)-1) + ")")
        for _, type_value := range type_values {
            vals = append(vals, type_value)
        }
    }
    
    if r.FormValue("number") != "" {
        number_values := CsvToList(r.FormValue("number"))
        conds = append(conds, "file.number in (?" + strings.Repeat(", ?", len(number_values)-1) + ")")
        for _, number_value := range number_values {
            vals = append(vals, number_value)
        }
    }

    if r.FormValue("page_max") != "" {
        page_max, err := strconv.Atoi(r.FormValue("page_max"))
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 422, "Can not read \"page_max\"")
            return
        }
        conds = append(conds, "file.pages <= ?")
        vals = append(vals, page_max)
    }
    
    if r.FormValue("page_min") != "" {
        page_min, err := strconv.Atoi(r.FormValue("page_min"))
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 422, "Can not read \"page_min\"")
            return
        }
        conds = append(conds, "file.pages >= ?")
        vals = append(vals, page_min)
    }
    
    if r.FormValue("words_max") != "" {
        words_max, err := strconv.Atoi(r.FormValue("words_max"))
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 422, "Can not read \"words_max\"")
            return
        }
        conds = append(conds, "file.word_count <= ?")
        vals = append(vals, words_max)
    }
    
    if r.FormValue("words_min") != "" {
        words_min, err := strconv.Atoi(r.FormValue("words_min"))
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 422, "Can not read \"words_min\"")
            return
        }
        conds = append(conds, "file.word_count >= ?")
        vals = append(vals, words_min)
    }

    // get files and process them
    log.Print("Get files from database")
    sql := "SELECT file.id, file.title_short, file.number, file.title_word_count, file.publish_date, file.type, file.author, file.file_size, file.word_count, file.insert_date, file.link, file.pages FROM file LEFT JOIN filekeyword AS fk ON file.id = fk.file_id LEFT JOIN keyword AS fkk ON fk.keyword_id = fkk.id LEFT JOIN filekeywordcontent AS fkc ON file.id = fkc.file_id LEFT JOIN keyword AS fkck ON fkc.keyword_id = fkck.id" + " WHERE " + strings.Join(conds, " AND ") + " GROUP BY file.id ORDER BY file.publish_date DESC LIMIT " + strconv.Itoa(pagination.Items) + " OFFSET " + strconv.Itoa((pagination.Page-1)*pagination.Items)
    log.Println(sql)
    //log.Println("vals=", vals)
    statement, err := db.Prepare(sql)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 422, "Invalid statement #1")
        return
    }
    rows, err := statement.Query(vals...)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #3")
        return
    }

    log.Print("Iterate over files")
    for rows.Next() {
        var file m.File
        err := rows.Scan(&file.Id, &file.Title, &file.Number, &file.TitleWordCount, &file.PublishDate, &file.Type, &file.Author, &file.FileSize, &file.WordCount, &file.InsertDate, &file.Link, &file.Pages)

        if err != nil {
            log.Print(err.Error())
        }

        files = append(files, file)
    }

    // pagination
    log.Print("Get pagination")
    sql = "SELECT COUNT(*) FROM (SELECT COUNT(*) FROM file LEFT JOIN filekeyword AS fk ON file.id = fk.file_id LEFT JOIN keyword AS fkk ON fk.keyword_id = fkk.id LEFT JOIN filekeywordcontent AS fkc ON file.id = fkc.file_id LEFT JOIN keyword AS fkck ON fkc.keyword_id = fkck.id WHERE " + strings.Join(conds, " AND ") + " GROUP BY file.id) dt"
    log.Println(sql)
    //log.Println("vals=", vals)
    count_query, err := db.Prepare(sql)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 422, "Invalid statement #2")
        return
    }
    count := count_query.QueryRow(vals...)
    var total_items int
    err = count.Scan(&total_items)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #2")
        return
    }

    pagination.Status = true
    pagination.TotalPages = int(math.Ceil(float64(total_items) / float64(pagination.Items)))
    log.Print(strconv.Itoa(total_items))

    response.Status = "success"
    response.Data = files
    response.Pagination = pagination
    json.NewEncoder(w).Encode(response)
}

func GetFilesLatest (w http.ResponseWriter, r *http.Request) {
    log.Print("GetFilesLatest() called")
    db, err := getDatabase()
    defer db.Close()
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #1")
        return
    }

    files := make([]m.File, 0)
    var response m.Response

    sql := "SELECT file.id, file.title_short, file.number, file.title_word_count, file.publish_date, file.type, file.author, file.file_size, file.word_count, file.insert_date, file.link, file.pages FROM file ORDER BY file.publish_date DESC LIMIT 30"
    rows, err := db.Query(sql)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #2")
        return
    }

    for rows.Next() {
        var file m.File
        err := rows.Scan(&file.Id, &file.Title, &file.Number, &file.TitleWordCount, &file.PublishDate, &file.Type, &file.Author, &file.FileSize, &file.WordCount, &file.InsertDate, &file.Link, &file.Pages)

        if err != nil {
            log.Print(err.Error())
        }

        files = append(files, file)
    }

    response.Data = files
    response.Status = "success"
    json.NewEncoder(w).Encode(response)
}