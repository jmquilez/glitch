from flask import Flask
import praw
import time
import os
import re
import pymongo
from threading import Thread
import certifi
from asyncpraw.models import MoreComments


app = Flask(__name__)
 
@app.route("/")
def home_view():
        print("HOMEVIEEEEEEW")
        return "<h1>Welcome!</h1><h2>You can check my Exway promo code:</h2><h2><a href='https://www.reddit.com/r/Exway/comments/jlh9p2/disc0unts_on_exway_boards_updated/?utm_medium=android_app&utm_source=share'>https://www.reddit.com/r/Exway/comments/jlh9p2/disc0unts_on_exway_boards_updated/?utm_medium=android_app&utm_source=share</a></h2>"

conn_str = "mongodb+srv://Exway_hawk_eye:shotsXAEA-XII12@cluster0.nqljd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)

try:
    print("CONNECTED TO DB SUCCESSFULLY!")
    print(client.server_info())
except Exception as e:
    print("Error connecting to db")
    print(e)

db = client.BigData
reddit = db.reddit

def bot_login():
    print("Logging in...")
    """r = praw.Reddit(username="exway_helper",
                    password="shotsXAEA-XII",
                    client_id="4FtGMK4rMK88zqRaEuRQ1A",
                    client_secret="i98VmtpRIO_XI6r5HNV5sI9jIRe17A",
                    user_agent="exway_helper",
                    redirect_uri="https://exway-hawk-eye.herokuapp.com/"
    )"""
    r = praw.Reddit(username="exway_assistance",
                    password="shotsXAEA-XII",
                    client_id="h4cGWai5sLcMT5GMyCacUw",
                    client_secret="mfZaY_rfN2AiRzqM5Tpef4P9FR0_mw",
                    user_agent="exway_assistance",
                    redirect_uri="https://exway-hawk-eye.herokuapp.com/"
                    )
    print(r.user.me())
    if r:
        print("Logged in!")
    else:
        print("ERROR LOGGING IN")

    return r

def run_bot(r, comments_replied_to):
    print("Searching last 1,000 comments")
    
    url = "https://www.reddit.com/r/allrandom69/comments/uondja/exway_bot/"
    submission = r.submission(url=url)
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():

        if re.search("Exway", comment.body, flags=re.I) and comment.id not in comments_replied_to and comment.author != r.user.me() and comment.author != r.redditor('Exway_hawk_eye'):
            print("comment found")
            print(comment.body)
            print("String with \"exway\" found in comment (id) " + comment.id)
            
            try:
                id = str(comment.author)
                r.redditor(id).message(subject = 'EXWAY SUPPORT TEAM', message = 'Hey there! Thanks for your support to Exway. If you end up buying a board and you ever have a problem just pm u/alxpht or reply here. Thanks bro :). Oh and btw it helps me a lot if you use my promo code: www.reddit.com/r/Exway/comments/jlh9p2/disc0unts_on_exway_boards_updated/')
                print("Replied to comment " + comment.id)
                comments_replied_to.append(comment.id)
                reddit.insert_one({ "id": comment.id })
            except Exception as e:
                print("Exception error, retrying: ")
                print(e)
        
    print("Search Completed.")
    print("Sleeping for 10 seconds...")
    # Sleep for 10 seconds...
    time.sleep(10)

def get_saved_comments():
    comments_replied_to = []
    found = reddit.find()
    for i in found:
        comments_replied_to.append(i["id"])

    return comments_replied_to


r = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)

def func():
    while True:
        run_bot(r, comments_replied_to)

Thread(target = func).start()
 
if __name__ == "__main__":
    app.run(use_reloader=False)
    