# Settings
The settings are nearly all saved in the `config.ini`
```
[database]
database = dbname
host = host
user = username
password = password
prefix = parlis_monitoring_

[logging]
level_console = 1
level_file = 2
filepath = parlis_monitoring_api.log
active = 1

[caching]
hours = 0
minutes = 1
```
This is a sample of the config file. 
`[datbase]` contains all the information to log into a mysql database. Use a prefix to avoid naming collisions.
`[logging]` contains logging information. This might not work with gunicorn. Use 0-2 for log level and 0-1 for active.
`[caching]` contains time for the cache. Just enter the time how long the cache should hold information.

> Change in the run.py the working directory. Therefore adapt the path in the `os.chdir` to your needs. 
{.is-warning}

# Installation
1. Copy the folder to your local storage
2. Set up a local redis server. If you want to use a remote one you'll have to adjust the connection directly in the run.py
3. Make sure you have installes all librarys needed and gunicorn
4. Adapt the settings to your needs
5. Run `bash startapi.bash`
6. Thats it, the api should now run under 127.0.0.1:8080

# Documentation
You can call the API via simple HTTP Get requests. There are several endpoints. 

All requests are default limited to only catch data from the last 183 days.

## Structure
Each file gets one entry containing
* date 
* type (e.g.: "Antrag", "kleine Anfrage")
* number (unique for each document, same as used from the government)

One file can contain multiple authors, authors are mostly political partys. They are listed with their short handle. "LRG" is short for "Landesregierung" (local government).

For each file there are many keywords referencing to the title (`files_keywords`) and othere referencing to the content of the PDF-File (`files_keywords_content`). 

## Endpoints

**Wordclouds**
`/wordclouds`

Returns the most used words for each author.

**Word by day**
`/wordbyday/{word}`

Returns a list of hits per day for the given word.

**Word by Day and Author**
`/wordbydayandauthor/{word}`

Returns a list of hits per day for the given word. Grouped for each author. 

**Word by Month**
`/wordbymonth/{word}`

Return a list of hits per month for the given word.

**Word by Month and Author**
`/wordbymonthandauthor/{word}`

Return a list of hits per month for the given word. Grouped for each author.

**Files by month**
`/filesbymonth`

Returns the amount of files created each month. 

**Search Files**
`/searchfiles`

Returns all files (max 500) matching the given parameters. 

Send parameteres with your Get-Request. You can use
* searchstring (matching file title)
* filenumber (matching the files number)
* type (matching the files type)
* date_begin (files that ar newer than this; use `YYYY-MM-DD` format)
* date_end (files that ar older than this; use `YYYY-MM-DD` format)
