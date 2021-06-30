import quart
import os
import requests


app = quart.Quart("")
app.secret_key = bytes(os.environ.get("session"), "utf-8")
