package main

import (
    "encoding/json"
    "net/http"
    "log"
    "github.com/gorilla/mux"
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
    "github.com/gorilla/handlers"
    "os"
    "errors"
    "time"
)

var db_password string
var db_user     string
var db_host     string
var db_table    string
var cors        []string

type ErrorMessage struct {
    Status  string  `json:"status"`
    Error   ErrorInfo   `json:"error"`
}

type ErrorInfo struct {
    Message string  `json:"message"`
}

func ErrorHandler(w http.ResponseWriter, r *http.Request, status_code int, message string) {
    log.Print("Internal Error: " + message)
    if status_code == 422 {
        w.WriteHeader(http.StatusUnprocessableEntity)
    } else if status_code == 503 {
        w.WriteHeader(http.StatusServiceUnavailable)
    } else {
        w.WriteHeader(http.StatusInternalServerError)
    }
    var e ErrorMessage
    var eInfo ErrorInfo
    e.Status = "error"
    eInfo.Message = message
    e.Error = eInfo

    json.NewEncoder(w).Encode(e)
}

func ErrorTest(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    ErrorHandler(w, r, 500, "Testfehlermeldung")
}

func getDatabase() (*sql.DB, error) {
    db, err := sql.Open("mysql", db_user + ":" + db_password + "@tcp(" + db_host + ")/" + db_table + "?parseTime=true")
    return db, err
}

func Ping(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("pong"))
}

func GetConfig() (error) {
    db_host = os.Getenv("PARLIS_API_DB_HOST")
    db_table = os.Getenv("PARLIS_API_DB_TABLE")
    db_password = os.Getenv("PARLIS_API_DB_PASSWORD")
    db_user = os.Getenv("PARLIS_API_DB_USER")
    cors_ := os.Getenv("PARLIS_API_CORS")

    if cors_ != "" {
        cors__ := CsvToList(cors_)
        for _, value := range cors__ {
            cors = append(cors, value)
        }
    } else {
        cors = append(cors, "*")
    }
    if db_host == "" || db_table == "" || db_user == "" {
        return errors.New("Missing one of those environmental variables: PARLIS_API_DB_HOST, PARLIS_API_DB_TABLE, PARLIS_API_DB_PASSWORD, PARLIS_API_DB_USER")
    }

    _, err := getDatabase()
    if err != nil {
        return err
    }
    return nil
}

func main() {
    err := GetConfig()
    if err != nil {
        log.Print(err.Error())
    }
    for err != nil {
        time.Sleep(10 * 60000 * time.Millisecond)
        err := GetConfig()
        if err != nil {
            log.Print(err.Error())
        }
    }

    log.Print("Up and running ...")

    r := mux.NewRouter()
    r.HandleFunc("/test/error", ErrorTest)
    r.HandleFunc("/ping", Ping)
    r.HandleFunc("/", Ping)
    r.HandleFunc("/stats", GetStats).Methods("GET")
    r.HandleFunc("/files", FilesSearch).Methods("POST")
    r.HandleFunc("/stats/backend", GetStatsBackend).Methods("GET")
    r.HandleFunc("/files/latest", GetFilesLatest).Methods("GET")
    r.HandleFunc("/authors", GetAuthors).Methods("GET")
    r.HandleFunc("/authors/stats", GetAuthorsStatistics).Methods("GET")
    r.HandleFunc("/types", GetTypes).Methods("GET")
    r.HandleFunc("/types/stats", GetTypesStatistics).Methods("GET")
    r.HandleFunc("/words/usage", GetWordsUsage).Methods("GET")
    r.HandleFunc("/words", GetWords).Methods("GET")

    headersOk := handlers.AllowedHeaders([]string{"X-Requested-With"})
    originsOk := handlers.AllowedOrigins(cors)
    methodsOk := handlers.AllowedMethods([]string{"GET", "HEAD", "POST", "PUT", "OPTIONS"})

    // Bind to a port and pass our router in
    log.Fatal(http.ListenAndServe(":8000", handlers.CORS(originsOk, headersOk, methodsOk)(r)))
}