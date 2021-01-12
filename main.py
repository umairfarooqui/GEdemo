import os
from flask import Flask, request
from google.cloud import storage
import logging

app = Flask(__name__)
# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = "test_bucket_14141"
@app.route('/', defaults={'path': 'data_docs/index.html'})
@app.route('/<path:path>')
def index(path):
    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    try:
        blob = bucket.get_blob(path)
        content = blob.download_as_string()
        print(content)
        if blob.content_encoding:
            resource = content.decode(blob.content_encoding)
        else:
            resource = content
    except Exception as e:
        logging.exception("couldn't get blob")
        resource = "<p></p>"
    return resource

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=int(os.environ.get('PORT', 8080)))