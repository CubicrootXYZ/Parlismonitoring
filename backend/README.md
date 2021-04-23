# The Backend

The backend is written in python and uses the "RNN Tagger" for text-stemming (the process for getting the root of a word). I am using this tool for getting a better understanding and knowledge about the topics and processes happening in the local government and parliament (research).

The `backend.py` runs 2 jobs:
- The Scraper
- The Tagger

The scraper gets the file list from the local government and inserts all metadata to the database.

The tagger parses the pdf file and tags all words with the "RNN Tagger". It collects some further metadata and inserts all that into the database. 

## Licensing

Please be aware, that the software used in this project might have restrictive licensing terms. Follow them! In general do not use this for commercial purposes.

Some licensing terms you should pay attention to:

* [RNN Tagger](https://www.cis.uni-muenchen.de/~schmid/tools/RNNTagger/Tagger-Licence) (Custom)
* [Pony ORM](https://www.apache.org/licenses/LICENSE-2.0) (Apache 2.0)
* [PDFPlumber](https://github.com/jsvine/pdfplumber/blob/stable/LICENSE.txt) (MIT)

You always can reach out to me via the communication channels provided on my webpage: [cubicroot.xyz](https://cubicroot.xyz)

## Settings
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
```

`database` contains all information to access the database.

`parlis` contains the URL of the scraped site. Please remind that this tool is optimized for one single url from the local government of Baden-Württtemberg. In the current state no other url is working - sorry. 

## Installation

Some quick thoughts you should know:

* Tagging via a neural network is very computationally expensive, but gives very good results
    * You might want to restrict resources for this process
* There are always failures in tagging!
* Do NOT spam requests to others infrastructure - this might also be permitted by law in your country
* Do respect local laws regarding copyright
    * This might be a little complicated, as this tool does not save any files on disk, only the stemmed words which are not suitable for reconstructing the original

### Via docker

Coming soon. Unfortunately due to licensing restrictions I am not allowed to share the docker image with you, but I will provide the Dockerfile.

Please be aware of the "bad performance" of "RNN Tagger" as it is NOT gpu accelerated with the provided Dockerfile. Neural networks generally behave A LOT BETTER with gpu acceleration. This project IS NOT MENT TO BE USED IN PRODUCTION.

### Manually

1. Install RNN Tagger and all its dependencies from [the official website](https://www.cis.uni-muenchen.de/~schmid/tools/RNNTagger/)
2. Clone this repository. 
3. Install the required pip packages from the `requirements.txt`
4. Adapt the `config.ini` to your needs.
5. Run the `backend.py` with python3.

## External Resources

Big thanks are going to developers and maintainers of the following software pieces:

* [RNN Tagger](https://www.cis.uni-muenchen.de/~schmid/tools/RNNTagger/) - Neural network for text stemming and more
* [Pony ORM](https://ponyorm.org/) - The ORM used in this project
* [Pdfplumber](https://github.com/jsvine/pdfplumber) - The PDF Parser
* [Requests](https://pypi.org/project/requests/) - HTTP request library
* and a lot more ...