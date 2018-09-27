short-shared-stories
====================

Short shared stories allows you to anonymously collaborate in creating very short stories.

It's main purpose is to demonstrate the difference between server- and client-rendered architecture. To that end, it's not a simple TODO app, but is still small enough to keep in your head.

## Running locally

Make sure you have Python 3.7, pipenv, and postgres installed. Navigate to this directory and run `pipenv install`. This will download all necessary python dependencies and create a virtual environment.

Make a postgres database called `short_shared_stories`. Run `pipenv shell` to get access to the virtual environment, then `python create_db.py` to make the tables.

Now you can run the app with `python main.py`.

Access the server-rendered app at localhost:5000

### Running the Client

If you want to run the client-rendered version, there are a couple more steps. You'll need to have `npm` and a recent-ish version of node installed.

Navigate to the client directory and run `npm install`. When that finishes, you should be able to run `npm run serve`.

Access the client-rendered app at localhost:8080
