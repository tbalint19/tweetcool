from flask import Flask, jsonify, g, current_app, request
import sqlite3
import time

app = Flask('Tweetcool server')
DATABASE = 'database.db'


# DB connector
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# Query runner
def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    cur.close()

    return (rv[0] if rv else None) if one else rv


def setup_db():
    query_db("""
    CREATE TABLE IF NOT EXISTS tweet(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        poster TEXT,
        content TEXT,
        timestamp INT
    )
    """)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def prevent_injection(value):
    return value.replace('"', '`').replace("'", '`').replace(';', ",")


#
# Routes
#
@app.route('/')
def connection_check():
    return 'It works!'


@app.route('/tweet', methods=['GET'])
def tweet_get():
    tweets = []
    where = ''
    limit = request.args.get('limit') or '10'
    offset = request.args.get('offset') or '0'
    poster = request.args.get('poster')
    from_timestamp = request.args.get('from')
    if poster:
        where += ' WHERE (poster = "' + poster + '") '
    if from_timestamp:
        where += (' AND ' if poster else ' WHERE ') + '(timestamp >= ' + from_timestamp + ')'
    for query in query_db('SELECT * FROM tweet ' + where + ' LIMIT ' + limit + ' OFFSET ' + offset):
        tweets.append({
            "id": query[0],
            "poster": query[1],
            "content": query[2],
            "timestamp": query[3]
        })

    resp = jsonify(*tweets)
    if len(tweets) == 1:
        resp.set_data('[\n' + resp.get_data().decode("utf-8").strip() + '\n]')
    if len(tweets) == 0:
        resp.set_data('[]')
    return resp


@app.route('/tweet', methods=['POST'])
def tweet_post():
    tweet = request.get_json()
    tweet["poster"] = prevent_injection(tweet["poster"][:20].strip())       # validation
    tweet["content"] = prevent_injection(tweet["content"][:144].strip())    # validation
    tweet["timestamp"] = int(time.time())

    query = """
            INSERT INTO tweet (poster, content, timestamp)
            VALUES ("{poster}", "{content}", {timestamp});
            """.format(**tweet)

    query_db(query)
    testing_query = query_db("SELECT * FROM tweet ORDER BY id DESC", one=True)

    return jsonify(**{
        "id": testing_query[0],
        "poster": testing_query[1],
        "content": testing_query[2],
        "timestamp": testing_query[3],
    })


with app.app_context():
    setup_db()
    print(current_app.name + ' started')
