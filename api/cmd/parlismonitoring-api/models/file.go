package models

/*
 * Tag... - a very simple struct
 */
type File struct {
    Id              NInt        `json:"id"`
    Title           NString     `json:"title"`
    Number          NString     `json:"number"`
    TitleWordCount  NInt        `json:"title_word_count"`
    PublishDate     NTime       `json:"publish_date"`
    Type            NString     `json:"type"`
    Author          NString     `json:"author"`
    FileSize        NInt        `json:"file_size"`
    WordCount       NInt        `json:"word_count"`
    InsertDate      NTime       `json:"insert_date"`
    Link            NString     `json:"link"`
    Pages           NInt        `json:"pages"`
}