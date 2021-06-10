# API 

Making the database accessible for the world :).

## Licensing

Keep an eye on the Licenses of the used libraries:

* [Gorilla/Mux](https://github.com/gorilla/mux/blob/master/LICENSE) (BSD 3-Clause "New" or "Revised" License)
* [Gorilla/Handlers](https://github.com/gorilla/handlers/blob/master/LICENSE) (BSD 2-Clause "Simplified" License)
* [Mysql](https://github.com/go-sql-driver/mysql/blob/master/LICENSE) (Mozilla Public License 2.0)

## Installing

### Docker 

An example Dockerfile is provided within this repository.

### Manually

* Install a recent go version
* Get requirements:

```
go get github.com/go-sql-driver/mysql
go get github.com/gorilla/mux
go get github.com/gorilla/handlers
```

* Build it

```
go build cmd/parlismonitoring-api/*.go
```

* Run the binary

## Endpoints

This is a list of endpoints and the data you can receive there.

### Copyright

It is not possible to retrieve whole documents through this API. Those are not even stored in the database. You only can search by the word-roots. 

Title's are capped at 160 signs. Why? Because german government thinks that this is a good idea: https://netzpolitik.org/2021/bundesregierung-gerichte-sollen-urheberrechtsreform-erklaeren/

### Unsuccessful responses

We generally use status code `500` for internal failures. If still possible there will be a status returned too. The `error` field holds more information, the message will always be set, other fields are optional.

### Pagination

Each successful response holds a "pagination" field. If it is used the `enabled` entry is set to `true`. 

Example Pagination:
```
{
    "status": ...,
    "data": ...,
    "pagination": 
    {
        "enabled": true,
        "page": 1,
        "total_pages": 12,
        "items_per_page": 10
    }
}
```

### Default Values

Values that are not available are either set to `null` or the corresponding golang default value. For all values where the difference between `null` and the default value (e.g. 0 for integers) matters the `null` is set for missing data.

Be aware that missing data might be updated later.

### Testing 

#### /test/error - GET/POST/PUT/DELETE

Returns an example error response

Response-Codes:

* `500`

Example Response:
```
{
   "status" : "error",
   "error" : {
      "message" : "Testfehlermeldung"
   }
}
```

### General Information

#### /stats - GET

General information about the data stored.

Method: `GET`

Response-Codes:

* `200` - Working as expected
* `500` - Internal Error
* `503` - Service not available

Example Response:
```
   "status" : "success",
   "data" : {
      "words" : 27671,
      "avrg_words" : 0,
      "authors" : 9,
      "biggest_words_title" : 44,
      "smallest_words" : 302,
      "smallest_title" : "Infektions-Rettungswagen",
      "files_total" : 75,
      "files_tagged" : 75,
      "biggest_file_size" : 500,
      "biggest_words" : 46926,
      "smallest_title_words" : 1,
      "avrg_file_size" : 500,
      "biggest_author" : "FDP/DVP",
      "avrg_title_words" : 3560.8267,
      "biggest_title" : "Entschließung zu der Regierungsinformation des Ministerpräsidenten im Nachgang der Konferenz der Bundeskanzlerin mit den Ministerpräsidentinnen und Ministerp..."
   },
   "pagination" : {
      "total_pages" : 0,
      "enabled" : false,
      "items_per_page" : 0,
      "page" : 0
   }
}
```

#### /stats/backend - GET

Information about the Backend. 

Method: `GET`

Response-Codes:

* `200` - Working as expected
* `500` - Internal Error
* `503` - Service not available

Example Response:
```
{
   "status" : "success",
   "pagination" : {
      "page" : 0,
      "total_pages" : 0,
      "enabled" : false,
      "items_per_page" : 0
   },
   "data" : {
      "scraper" : {
         "avrg_time" : 1300043,
         "files_processed" : 54,
         "status" : "started",
         "last_run" : "2021-04-05T12:07:50Z",
         "avrg_files" : 54
      },
      "tagger" : {
         "avrg_files" : null,
         "last_run" : null,
         "status" : "started",
         "files_processed" : null,
         "avrg_time" : null
      }
   }
}
```

### Files

#### /files/latest - GET

Returns the latest 30 files.

Method: `GET`

Response-Codes:

* `200` - Working as expected
* `500` - Internal Error
* `503` - Service not available

Example Response:
```
{
   "status" : "success",
   "pagination" : {
      "enabled" : false,
      "total_pages" : 0,
      "items_per_page" : 0,
      "page" : 0
   },
   "data" : [
      {
         "word_count" : 2514,
         "id" : 1,
         "author" : "FDP/DVP",
         "insert_date" : "2021-03-21T11:00:27Z",
         "link" : "https://www.landtag-bw.de/files/live/sites/LTBW/files/dokumente/WP16/Drucksachen/9000/16_9708_D.pdf",
         "file_size" : null,
         "title_word_count" : 5,
         "number" : "16/9708",
         "pages" : 8,
         "type" : "Kleine Anfrage",
         "title" : "Erschließungsbeitragsrechtlich relevante Straßen im Enzkreis",
         "publish_date" : "2021-03-19T00:00:00Z"
      },
      ...
   ]
}
```

#### /files - POST

Search for files

Method: `POST`

Parameters:

`page`: the current page `default: 1`

`title`: Comma separated keywords to search for (combined with or) `optional`

`content`: Comma separated keywords to search for in the file content `optional`

`author`: Comma separated authors to search for (combined with or) `optional`

`start`: Date to begin search with in format YYYY-MM-DD `optional`, `default: DATE_SUB(NOW(), INTERVAL 182 DAY)`

`end`: Date to end the search with in format YYYY-MM-DD `optional`

`type`: Comma separated types to search for (combined with or) `optional`

`number`: Comma separated document number to search for (combined with or) `optional`

`page_max`: Maximum pages of the document `optional`

`page_min`: Minimum pages of the document `optional`

`words_max`: Maximum words of the document `optional`

`words_min`: Minimum words of the document `optional`

Response-Codes:

* `200` - Working as expected
* `422` - Required Parameters not set or invalid
* `500` - Internal Error
* `503` - Service not available

Example Response:
```
{
   "data" : [
      {
         "pages" : null,
         "word_count" : 8923,
         "file_size" : null,
         "publish_date" : "2021-03-09T00:00:00Z",
         "type" : "Alle",
         "link" : "https://www.landtag-bw.de/files/live/sites/LTBW/files/dokumente/WP16/Drucksachen/9000/16_9392_D.pdf",
         "insert_date" : "2021-03-21T11:00:33Z",
         "author" : "LRG",
         "number" : "16/9392",
         "title" : "Bericht der Landesregierung nach § 7 Absatz 3 Gesetz zur Förderung des Klimaschutzes in Baden-Württemberg",
         "id" : 69,
         "title_word_count" : 15
      }
   ],
   "status" : "success",
   "pagination" : {
      "page" : 1,
      "enabled" : true,
      "items_per_page" : 50,
      "total_pages" : 1
   }
}
```

### Authors

#### /authors - GET

Returns a list of all authors

Method: `GET`

Response-Codes:

* `200` - Working as expected
* `500` - Internal Error
* `503` - Service not available

Example Response:
```
{
   "status" : "success",
   "pagination" : {
      "total_pages" : 0,
      "items_per_page" : 0,
      "enabled" : false,
      "page" : 0
   },
   "data" : [
      "FDP/DVP",
      "GRÜNE",
      "Fraktionslos",
      "SPD",
      "LRG",
      "AfD",
      "Ausschüsse",
      "CDU",
      "GRÜNE, CDU"
   ]
}
```

#### /authors/statistics - GET

Returns some statistic values on author-base

Method: `GET`

Response-Codes:

* `200` - Working as expected
* `500` - Internal Error
* `503` - Service not available

Example Response:
```
{
   "data" : {
      "Fraktionslos" : {
         "author" : "Fraktionslos",
         "files" : 3,
         "last_publish_date" : "2021-03-19T00:00:00Z"
      },
      "SPD" : {
         "author" : "SPD",
         "files" : 21,
         "last_publish_date" : "2021-03-19T00:00:00Z"
      },
      "GRÜNE" : {
         "last_publish_date" : "2021-03-19T00:00:00Z",
         "author" : "GRÜNE",
         "files" : 3
      },
      "GRÜNE, CDU" : {
         "author" : "GRÜNE, CDU",
         "files" : 1,
         "last_publish_date" : "2021-03-09T00:00:00Z"
      },
      "Ausschüsse" : {
         "author" : "Ausschüsse",
         "files" : 1,
         "last_publish_date" : "2021-03-18T00:00:00Z"
      },
      "CDU" : {
         "last_publish_date" : "2021-03-10T00:00:00Z",
         "author" : "CDU",
         "files" : 1
      },
      "AfD" : {
         "author" : "AfD",
         "files" : 12,
         "last_publish_date" : "2021-03-18T00:00:00Z"
      },
      "FDP/DVP" : {
         "last_publish_date" : "2021-03-19T00:00:00Z",
         "files" : 23,
         "author" : "FDP/DVP"
      },
      "LRG" : {
         "author" : "LRG",
         "files" : 10,
         "last_publish_date" : "2021-03-18T00:00:00Z"
      }
   },
   "status" : "success",
   "pagination" : {
      "enabled" : false,
      "items_per_page" : 0,
      "page" : 0,
      "total_pages" : 0
   }
}
```

### Types

#### /types - GET

Returns a list of all types

Method: `GET`

Response-Codes:

* `200` - Working as expected
* `500` - Internal Error
* `503` - Service not available

Example Response:
```
{
   "data" : [
      "Kleine Anfrage",
      "Alle",
      "Antrag",
      "Beschlussempfehlung"
   ],
   "pagination" : {
      "enabled" : false,
      "items_per_page" : 0,
      "page" : 0,
      "total_pages" : 0
   },
   "status" : "success"
}
```

#### /types/statistics - GET

Returns some statistic values on type-base

Method: `GET`

Response-Codes:

* `200` - Working as expected
* `500` - Internal Error
* `503` - Service not available

Example Response:
```
{
   "pagination" : {
      "enabled" : false,
      "items_per_page" : 0,
      "page" : 0,
      "total_pages" : 0
   },
   "status" : "success",
   "data" : {
      "Antrag" : {
         "files" : 17,
         "author" : "Antrag",
         "last_publish_date" : "2021-03-18T00:00:00Z"
      },
      "Beschlussempfehlung" : {
         "author" : "Beschlussempfehlung",
         "last_publish_date" : "2021-03-18T00:00:00Z",
         "files" : 1
      },
      "Alle" : {
         "author" : "Alle",
         "last_publish_date" : "2021-03-18T00:00:00Z",
         "files" : 10
      },
      "Kleine Anfrage" : {
         "files" : 47,
         "last_publish_date" : "2021-03-19T00:00:00Z",
         "author" : "Kleine Anfrage"
      }
   }
}
```

### Words

#### /words - GET

Returns the type of a word.

Method: `GET`

Parameters: 

`word`: Comma separated words to search for.

Response-Codes:

* `200` - Working as expected
* `422` - Can not read input
* `500` - Internal Error
* `503` - Service not available

Example Response:
```
{
  "status": "success",
  "data": [
    "noun",
    "adjective"
  ],
  "pagination": {
    "enabled": false,
    "page": 0,
    "total_pages": 0,
    "items_per_page": 0
  }
}
```

#### /words/usage - GET

Returns time series of usages of the words given

Method: `GET`

Parameters: 

`word`: Comma separated words to search for.

Response-Codes:

* `200` - Working as expected
* `422` - Can not read input
* `500` - Internal Error
* `503` - Service not available

Example Response:
```
{
  "status": "success",
  "data": {
    "2021-03-09": 7,
    "2021-03-10": 14,
    "2021-03-11": 47,
    "2021-03-12": 16,
    "2021-03-15": 16,
    "2021-03-16": 34,
    "2021-03-18": 994,
    "2021-03-19": 20
  },
  "pagination": {
    "enabled": false,
    "page": 0,
    "total_pages": 0,
    "items_per_page": 0
  }
}
```

## Attribution

Great thanks to the developers of following software that is used in this project:

* [Gorilla/Mux](https://github.com/gorilla/mux/)
* [Gorilla/Handlers](https://github.com/gorilla/handlers)
* [Mysql](https://github.com/go-sql-driver/mysql)

And all the others not mentioned here.