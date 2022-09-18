from flask import Flask
import praw
import time
import os
import re
import pymongo
from threading import Thread
import certifi
from asyncpraw.models import MoreComments
from Reddit_ChatBot_Python import ChatBot, RedditAuthentication
from Reddit_ChatBot_Python import CustomType, Snoo, Reaction
import ssl

app = Flask(__name__)
 
@app.route("/")
def home_view():
        print("HOMEVIEEEEEEW")
        return "<h1>Welcome!</h1><h2>You can check my Exway promo code:</h2><h2><a href='https://www.reddit.com/r/Exway/comments/jlh9p2/disc0unts_on_exway_boards_updated/?utm_medium=android_app&utm_source=share'>https://www.reddit.com/r/Exway/comments/jlh9p2/disc0unts_on_exway_boards_updated/?utm_medium=android_app&utm_source=share</a></h2>"

conn_str = "mongodb+srv://Exway_hawk_eye:shotsXAEA-XII12@cluster0.nqljd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)

reddit_authentication = RedditAuthentication.PasswordAuth(reddit_username="Random_usersfx", reddit_password="ESTAFADOR45", twofa=None)

chatbot = ChatBot(print_chat=True, store_session=True, log_websocket_frames=False, authentication=reddit_authentication)

#chatbot.enable_rate_limiter(max_calls=23, period=1.5)

try:
    print("CONNECTED TO DB SUCCESSFULLY!")
    print(client.server_info())
except Exception as e:
    print("Error connecting to db")
    print(e)

db = client.BigData
reddit = db.r1

def bot_login():
    print("Logging in...")
    """r = praw.Reddit(username="exway_assistance",
                    password="exway284agc",
                    client_id="x5lxnULe7oaYw-takx7uBQ",
                    client_secret="4BzMjGh10NWevxtnxb9m07Qv1HjUlg",
                    user_agent="exway_assistance",
                    redirect_uri="https://exway-hawk-eye.herokuapp.com/"
                    )"""
    r = praw.Reddit(username="exway-helper",
                    password="shotsXAEA-XII12",
                    client_id="JxdBVsEQbWMLG9XAAnePog",
                    client_secret="gB7IjdnzFzBlShmJ0Qf8T9tojyNraA",
                    user_agent="exway-helper",
                    redirect_uri="https://exway-hawk-eye.herokuapp.com/"
                    )
    print(r.user.me())
    if r:
        print("Logged in!")
    else:
        print("ERROR LOGGING IN")

    return r

err_ans = []

def run_bot(r, comments_replied_to):
    print("Searching last 1,000 comments")
    
    url = "https://www.reddit.com/r/ElectricSkateboarding/comments/n28k7u/recommendations_and_suggestions/"
    submission = r.submission(url=url)
    submission.comment_sort = 'new'
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        
        if re.search("Exway", comment.body, flags=re.I) and comment.id not in comments_replied_to and comment.author != r.user.me() and comment.created_utc > 1652545159.0:
            
            print("comment found")
            print(comment.body)
            print(comment.created_utc)
            print("String with \"exway\" found in comment (id) " + comment.id)
            
            try:
                id = str(comment.author)
                #r.redditor(id).message(subject = 'EXWAY SUPPORT TEAM', message = 'Hey there! Thanks for your support to Exway. If you end up buying a board and you ever have a problem just pm u/alxpht or reply here. Thanks bro :). Oh and btw it helps me a lot if you use my promo code: www.reddit.com/r/Exway/comments/jlh9p2/disc0unts_on_exway_boards_updated/')
                dm1(id)
                print("Replied to comment " + comment.id)
                print("Receiver was: " + id)
                comments_replied_to.append(comment.id)
                reddit.insert_one({ "id": comment.id, "author": comment.author.name, "url": comment.permalink, "timestamp": comment.created_utc, "err_message": "None"})
            except Exception as e:
                print(err_ans)
                corr = False
                if len(err_ans) > 0:
                    for i in err_ans:
                        if i["id"] == comment.id:
                            corr = True
                            i["n"]+=1
                            if i["n"] >= 3:
                                err_ans.remove(i)
                                comments_replied_to.append(comment.id)
                                reddit.insert_one({ "id": comment.id, "author": comment.author.name, "url": comment.permalink, "timestamp": comment.created_utc, "err_message": str(e)})
                    if corr == False:
                        err_ans.append({"id": comment.id, "n": 0})
                else:
                    err_ans.append({"id": comment.id, "n": 0})

                print("Exception error, retrying: ")
                print(e)
                print(err_ans)
        
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
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
    # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
    
    while True:
        run_bot(r, comments_replied_to)

"""@chatbot.event.on_ready
def dm(_):
    print('GOING ON')
    dm_channel = chatbot.create_direct_channel("New_Finalizer_28")
    chatbot.send_message('Hey there!', dm_channel.channel_url)
    chatbot.send_message('Thanks for your support to Exway. If you end up buying a board and you ever have a problem just pm u/alxpht or reply here. Thanks bro :)', dm_channel.channel_url)
    chatbot.send_message('Oh and btw it helps me a lot if you use my promo code: www.reddit.com/r/Exway/comments/jlh9p2/disc0unts_on_exway_boards_updated/', dm_channel.channel_url)"""

def dm1(id):
    dm_channel = chatbot.create_direct_channel(id)
    chatbot.send_message('Hey there!', dm_channel.channel_url)
    chatbot.send_message('Thanks for your support to Exway. If you end up buying a board and you ever have a problem just pm u/alxpht or reply here. Thanks bro :)', dm_channel.channel_url)
    chatbot.send_message('Oh and btw it helps me a lot if you use my promo code: www.reddit.com/r/Exway/comments/jlh9p2/disc0unts_on_exway_boards_updated/', dm_channel.channel_url)

Thread(target = func).start()
chatbot.run_4ever(auto_reconnect=True, disable_ssl_verification=True)
 
if __name__ == "__main__":
    app.run(use_reloader=False)