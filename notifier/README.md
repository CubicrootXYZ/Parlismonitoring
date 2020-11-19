# PARLISnotifier

Simple notifier for new files. 

## Settings

### Database

`database`: name of database

`host`: host of database

`user` and `password`: credentials for loging in to the database

`prefix`: prefix for all tables

## Search

`title_keywords`: comma separated keywords in file titles that you will be sent notifications for (do not use spaces)

`content_keywords`: comma separated keywords in file content that you will be sent notifications for (do not use spaces)

`laws`: 1 to be notified for new laws (Gesetzesbeschlüsse und -entwürfe), 0 to ignore

`intervall_days`: how many days in past files should be included (adapt that to your cronjob intervall)

## Mail

`mailto`: mail address to mail notifications to

`host`: smtp host

`user` and `password`: smtp credentials

`port`: smtp port

## Installation

Run the `run.py` via a cronjob
