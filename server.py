from flask import Flask, request, Response

from migrator import migrator

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        f = request.files["file"]
        if f:
            raw_file = f.read().decode("utf-8")
            migrated = migrator(raw_file)
            return Response(migrated, mimetype="text/plain")
    return """
    <!doctype html>
    <title>intl fixer</title>
    <h1>intl fixer</h1>
    <form action="" method=post enctype=multipart/form-data>

        <p><input type=file name=file>

        <input type=submit value=Upload>    
    </form>
    """
