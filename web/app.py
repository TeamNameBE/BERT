from web.routes.utils import app
from quart import Quart, redirect, url_for, render_template, request


app = Quart(__name__)


@app.route("/")
async def home():
    return await render_template("index.html")
