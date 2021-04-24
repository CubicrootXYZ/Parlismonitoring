package main

import (
    "encoding/json"
    "log"
    "net/http"
    m "./models"
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
    "errors"
)

func GetStats(w http.ResponseWriter, r *http.Request) {
    log.Print("GetStats() called")
    w.Header().Set("Content-Type", "application/json")  // always return JSON
    var response m.Response
    response.Status = "success"

    db, err := getDatabase()
    defer db.Close()
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #1")
        return
    }

    var stats m.Stats

    total := db.QueryRow("SELECT COUNT(title) FROM file")
    err = total.Scan(&stats.TotalFiles)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #2")
        return
    }

    total_tagged := db.QueryRow("SELECT COUNT(title) FROM file WHERE word_count IS NOT NULL")
    err = total_tagged.Scan(&stats.TaggedFiles)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #3")
        return
    }

    authors := db.QueryRow("SELECT COUNT(DISTINCT author) FROM file")
    err = authors.Scan(&stats.Authors)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #4")
        return
    }

    words := db.QueryRow("SELECT COUNT(DISTINCT word) FROM keyword")
    err = words.Scan(&stats.Words)
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #5")
        return
    }

    avg_size := db.QueryRow("SELECT AVG(file_size) FROM file WHERE file_size IS NOT NULL")
    if avg_size != nil {
        err = avg_size.Scan(&stats.AvgSize)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #6")
            return
        }
    }

    avg_title_words := db.QueryRow("SELECT AVG(title_word_count) FROM file WHERE title_word_count IS NOT NULL")
    if avg_title_words != nil {
        err = avg_title_words.Scan(&stats.AvgTitleWords)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #7")
            return
        }
    }
    
    avg_words := db.QueryRow("SELECT AVG(word_count) FROM file WHERE word_count IS NOT NULL")
    if avg_words != nil {
        err = avg_words.Scan(&stats.AvgWords)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #8")
            return
        }
    }

    b_author := db.QueryRow("SELECT author FROM file GROUP BY author ORDER BY COUNT(id) DESC LIMIT 1")
    if b_author != nil {
        err = b_author.Scan(&stats.BiggestAuthor)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #9")
            return
        }
    }

    b_file_size := db.QueryRow("SELECT MAX(file_size) FROM file")
    if b_file_size != nil {
        err = b_file_size.Scan(&stats.BiggestFileSize)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #10")
            return
        }
    }

    b_words := db.QueryRow("SELECT MAX(word_count) FROM file")
    if b_words != nil {
        err = b_words.Scan(&stats.BiggestWords)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #11")
            return
        }
    }
    
    b_words_title := db.QueryRow("SELECT MAX(title_word_count) FROM file")
    if b_words_title != nil {
        err = b_words_title.Scan(&stats.BiggestWordsTitle)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #12")
            return
        }
    }

    b_title := db.QueryRow("SELECT title_short FROM file ORDER BY title_word_count DESC LIMIT 1")
    if b_title != nil {
        err = b_title.Scan(&stats.BiggestTitle)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #13")
            return
        }
    }

    s_words := db.QueryRow("SELECT MIN(word_count) FROM file")
    if s_words != nil {
        err = s_words.Scan(&stats.SmallestWords)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #14")
            return
        }
    }

    s_title_words := db.QueryRow("SELECT MIN(title_word_count) FROM file")
    if s_title_words != nil {
        err = s_title_words.Scan(&stats.SmallestTitleWords)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #15")
            return
        }
    }

    s_title := db.QueryRow("SELECT title_short FROM file WHERE title_word_count IS NOT NULL ORDER BY title_word_count ASC LIMIT 1")
    if s_title != nil {
        err = s_title.Scan(&stats.SmallestTitle)
        if err != nil {
            log.Print(err.Error())
            ErrorHandler(w, r, 503, "Datenbankfehler #16")
            return
        }
    }

    response.Data = stats

    json.NewEncoder(w).Encode(response)
}

func GetStatsBackend(w http.ResponseWriter, r *http.Request) {
    log.Print("GetStatsBackend() called")
    w.Header().Set("Content-Type", "application/json")  // always return JSON
    var response m.Response

    scraper, err := GetStatsBackendByBackend("scrape")
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #1")
        return
    }
    tagger, err := GetStatsBackendByBackend("tag")
    if err != nil {
        log.Print(err.Error())
        ErrorHandler(w, r, 503, "Datenbankfehler #2")
        return
    }

    data := make(map[string]*m.StatsProcess)  // wtf go is weird, need pointers to marshal correctly
    data["scraper"] = &scraper
    data["tagger"] = &tagger
    response.Data = data
    response.Status = "success"
    json.NewEncoder(w).Encode(response)
}

func GetStatsBackendByBackend(backend string) (m.StatsProcess, error) {
    var stats m.StatsProcess

    db, err := getDatabase()
    defer db.Close()
    if err != nil {
        log.Print(err.Error())
        return stats, errors.New("Datenbankfehler #1")
    }

    last_run := db.QueryRow("SELECT end FROM " + backend + " WHERE end IS NOT NULL ORDER BY end desc LIMIT 1")
    if last_run != nil {
        err = last_run.Scan(&stats.LastRun)
        if err == sql.ErrNoRows {
            //skip
        } else if err != nil {
            log.Print(err.Error())
            return stats, errors.New("Unbekannter Datenbankfehler")
        }
    }

    files := db.QueryRow("SELECT processed_files FROM " + backend + " WHERE processed_files IS NOT NULL ORDER BY end desc LIMIT 1")
    if files != nil {
        err = files.Scan(&stats.FilesProcessed)
        if err == sql.ErrNoRows {
            //skip
        } else if err != nil {
            log.Print(err.Error())
            return stats, errors.New("Unbekannter Datenbankfehler")
        }
    }

    avrg_files := db.QueryRow("SELECT AVG(processed_files) FROM " + backend + " WHERE processed_files IS NOT NULL")
    if avrg_files != nil {
        err = avrg_files.Scan(&stats.AvrgFiles)
        if err == sql.ErrNoRows {
            //skip
        } else if err != nil {
            log.Print(err.Error())
            return stats, errors.New("Unbekannter Datenbankfehler")
        }
    }
    
    avrg_time := db.QueryRow("SELECT TIME_TO_SEC(AVG(TIMEDIFF(end, start))) FROM " + backend + " WHERE start IS NOT NULL AND end IS NOT NULL")
    if avrg_time != nil {
        err = avrg_time.Scan(&stats.AvrgTime)
        if err == sql.ErrNoRows {
            //skip
        } else if err != nil {
            log.Print(err.Error())
            return stats, errors.New("Unbekannter Datenbankfehler")
        }
    }

    status := db.QueryRow("SELECT status FROM " + backend + " WHERE start IS NOT NULL AND status IS NOT NULL")
    if status != nil {
        err = status.Scan(&stats.Status)
        if err == sql.ErrNoRows {
            //skip
        } else if err != nil {
            log.Print(err.Error())
            return stats, errors.New("Unbekannter Datenbankfehler")
        }
    }

    return stats, nil
}