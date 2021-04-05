package models

type Stats struct {
    TotalFiles          int     `json:"files_total"`
    TaggedFiles         int     `json:"files_tagged"`
    Authors             int     `json:"authors"`
    Words               int     `json:"words"`
    AvgSize             float64 `json:"avrg_file_size"`
    AvgTitleWords       float64 `json:"avrg_title_words"`
    AvgWords            float64 `json:"avrg_words"`
    BiggestAuthor       string  `json:"biggest_author"`
    BiggestFileSize     int     `json:"biggest_file_size"`
    BiggestWords        int     `json:"biggest_words"`
    BiggestWordsTitle   int     `json:"biggest_words_title"`
    BiggestTitle        string  `json:"biggest_title"`
    SmallestWords       int     `json:"smallest_words"`
    SmallestTitleWords  int     `json:"smallest_title_words"`
    SmallestTitle       string  `json:"smallest_title"`
}

type StatsProcess struct {
    LastRun         NTime   `json:"last_run"`
    FilesProcessed  NInt    `json:"files_processed"`
    AvrgFiles       NFloat  `json:"avrg_files"`
    AvrgTime        NFloat  `json:"avrg_time"`
    Status          NString `json:"status"`
}