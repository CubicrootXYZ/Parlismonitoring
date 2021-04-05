package main

import (
    "strings"
)

func CsvToList(csv string) ([]string) {
    words := strings.Split(csv, ",")

    for i, _ := range words {
        words[i] = strings.TrimSpace(words[i])
    }

    return words
}