import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running!"

def run_bot():
    # make sure 'main.py' is your bot entry file
    os.system("python3 main.py")

if __name__ == "__main__":
    # Run your bot in a background thread
    threading.Thread(target=run_bot).start()

    # Universal port detection
    # - Render → gives random port in $PORT
    # - Koyeb  → expects 8000
    # - Heroku → gives random port in $PORT
    port = int(os.environ.get("PORT", 8000))

    app.run(host="0.0.0.0", port=port)
    
