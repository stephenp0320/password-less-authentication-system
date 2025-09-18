import os
from flask import Flask 
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", "8000"))
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
 
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=[FRONTEND_ORIGIN])


@app.get("/ping")
def ping():
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)


