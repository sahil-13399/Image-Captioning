import os
import glob
from flask import Flask, request, render_template, send_from_directory
from gen_cap import ret_cap

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def hello_world():
    return render_template("upload.html")


@app.route('/upload', methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    files = glob.glob(target+'/*')
    for f in files:
        os.remove(f)

    for upload in request.files.getlist("image"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    #caption = ret_cap("./images/"+filename)
    caption = ret_cap(destination)

    return render_template("complete.html", image_name=filename, caption=caption)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == '__main__':
    app.run(debug=True)
