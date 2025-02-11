import io

from flask import Flask, render_template, send_file
from sqlalchemy import select
from sqlalchemy.orm import Session
from wordcloud import STOPWORDS, WordCloud

from src.db import Labels, engine

app = Flask(__name__)
session = Session(engine)


def generate_wordcloud(text):
    stopwords = set(STOPWORDS)

    wc = WordCloud(
        stopwords=stopwords,
        background_color="#424242",
        colormap="GnBu",
        width=800,
        height=500,
    )
    wc.generate(text)

    output = io.BytesIO()
    wc.to_image().save(output, format="PNG")
    output.seek(0)
    return send_file(output, mimetype="image/png")


@app.route("/sar.png")
def sar_wc():
    result = session.execute(select(Labels.sar)).fetchall()
    return generate_wordcloud(" ".join([row[0] for row in result]))


@app.route("/work.png")
def work_wc():
    result = session.execute(select(Labels.work)).fetchall()
    return generate_wordcloud(" ".join([row[0] for row in result]))


@app.route("/home.png")
def home_wc():
    result = session.execute(select(Labels.home)).fetchall()
    return generate_wordcloud(" ".join([row[0] for row in result]))


@app.route("/")
def index():
    return render_template("index.html")
