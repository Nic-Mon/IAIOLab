# IAIOLAB - 78 RPM Record player

## Description
A playlist and front-end for discovering and listening to 78 RPM records in the Internet Archive's collection.

## How to run
To set up the database instance, open a shell at the IAIOLab folder and type:
  
  sqlite3 app.db < schema.sql -echo

Every time you want to start the server (with the same data intact) just go to the same location and type:

  python run.py

The RUNME.sh script combines these steps for your convenience.
