from flask import Flask
import asyncio

app = Flask(__name__)

@app.route('/')
async def hello():
    return 'Hello, async world!'
