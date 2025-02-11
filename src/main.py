import io

from flask import Flask, redirect, render_template, request, send_file, url_for
from sqlalchemy import select
from sqlalchemy.orm import Session
from wordcloud import STOPWORDS, WordCloud

from src.db import Labels, engine

app = Flask(__name__)


def generate_wordcloud(text: str):
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
    with engine.connect() as conn:
        result = conn.execute(select(Labels.sar)).fetchall()
    return generate_wordcloud(" ".join([row[0] for row in result]))


@app.route("/work.png")
def work_wc():
    with engine.connect() as conn:
        result = conn.execute(select(Labels.work)).fetchall()
    return generate_wordcloud(" ".join([row[0] for row in result]))


@app.route("/home.png")
def home_wc():
    with engine.connect() as conn:
        result = conn.execute(select(Labels.home)).fetchall()
    return generate_wordcloud(" ".join([row[0] for row in result]))


@app.route("/")
def index():
    images = [
        ("When we are in SAR", "sar", "/sar.png"),
        ("When we are at work", "work", "/work.png"),
        ("When we are at home", "home", "/home.png"),
    ]
    return render_template("index.html", images=images)


@app.route("/create", methods=["POST"])
def add_record():
    if request.form["sar"] and request.form["work"] and request.form["home"]:
        with Session(engine) as session:
            label = Labels(
                sar=request.form["sar"].lower(),
                work=request.form["work"].lower(),
                home=request.form["home"].lower(),
            )
            session.add(label)
            session.commit()

    return redirect(url_for("index"))
