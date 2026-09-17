from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Manoj AWS DevOps Project</title>
        </head>
        <body>
            <h1>AWS DevOps CI/CD Project</h1>
            <p>Application deployed automatically using Jenkins CI/CD.</p>            <p>Author: Manoj</p>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
