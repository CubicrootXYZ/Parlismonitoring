# Settings
The `config.ini` file should look like this:
```
[database]
database = dbname
host = host
user = username
password = password
prefix = parlis_monitoring_

[parlis]
url = https://www.landtag-bw.de/cms/render/live/de/sites/LTBW/home/dokumente/drucksachen/contentBoxes/drucksachen.xhr?limit=30&initiativeType=&offset=

[logging]
level_console = 1
level_file = 2
filepath = parlis_monitoring.log
active = 1
```

`database` contains all information to access the database.

`parlis` contains the URL of the scraped site. Please remind that this tool is optimized for one single url from the local government of Baden-Württtemberg. You might also change for which content to look when using another url. 

`[logging]` contains logging information. This might not work with gunicorn. Use 0-2 for log level and 0-1 for active.

# Installation
1. Copy the files to your local folder.
2. Change the `os.chdir` to your working directory, this is the path to the folder where the run.py is. 
3. Make sure to have installed all needed packages. Especially `bs4`, `PyPDF2`, `io`, `spacy` with german stemmer and lemmatizer are needed. This tool runs with python 3.
4. Run `run.py` as a daemon. You might use `systemd` for that. It automatically scrapes Monday-Friday from 6-16 o`clock. 
