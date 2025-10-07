from flask import Flask, request, jsonify
from flask-cors import CORS
from pytranscribe import transcribe_audio
from sentiment import analyze_sentiment
