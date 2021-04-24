package models

/*
 * A response object
 */
type Response struct {
    Status      string      `json:"status"`
    Data        interface{} `json:"data"`
    Pagination  Pagination  `json:"pagination"`
}

type Pagination struct {
    Status      bool    `json:"enabled"`
    Page        int     `json:"page"`
    TotalPages  int     `json:"total_pages"`
    Items       int     `json:"items_per_page"`
}