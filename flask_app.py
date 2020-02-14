from flask import Flask, request, redirect
import json
from project_list import ProjectList
from project import Project
import os, os.path

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

@app.route("/", methods=["GET", "POST"])
def __main__():
    errors = ""
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'static/picturesjpeg/')
    THIS_FOLDER2 = os.path.dirname(os.path.abspath(__file__))
    project_all = os.path.join(THIS_FOLDER2, 'static/projects.txt')
    with open(project_all, "r") as read_list:
        project_list = json.load(read_list)


    def allowed_file(filename):
        if '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                return True

    def change_pics(picurl, id):
        project_all = os.path.join(THIS_FOLDER2, 'static/projects.txt')
        with open(project_all, "r") as read_all:
            project_list = json.load(read_all)
        project_detail = os.path.join(THIS_FOLDER, 'static/projectdetails/project' + str(project_list["data"][-1]["monument_id"]) + '.txt')
        with open(project_detail, "r") as read_details:
            project_details = json.load(read_details)
        project_picture = os.path.join(THIS_FOLDER, 'static/projectpictures/picsproject' + str(project_list["data"][-1]["monument_id"]) + '.txt')
        with open(project_picture, "r") as read_pics:
            project_pics = json.load(read_pics)

        index = int(project_details["data"]["transboundary"])
        for x in range(index):
            if project_pics["data"][x]["picture_url"] is "":
                project_pics["data"][x]["picture_url"] = picurl
                break
        projects_pic = open(project_picture, "w")
        projects_pic.write(json.dumps(project_pics))
        projects_pic.close()

        project_details["data"]["thumbnail"] = picurl
        projects_det = open(project_detail, "w")
        projects_det.write(json.dumps(project_details))
        projects_det.close()

        project_list["data"][-1]["thumbnail"] = picurl
        projects_file = open(project_all, "w")
        projects_file.write(json.dumps(project_list))
        projects_file.close()

    if request.method == "POST":
        pics = None
        name = None
        lat = None
        lon = None
        state = None
        product = None
        year = None
        desc = None

        try:
            name = str(request.form["field1"])
        except:
            errors += "<p>{!r} is not a valid name.</p>\n".format(request.form["field1"])
        try:
            lat = float(request.form["field2"])
        except:
            errors += "<p>{!r} is not a valid value.</p>\n".format(request.form["field2"])
        try:
            lon = float(request.form["field3"])
        except:
            errors += "<p>{!r} is not a valid value.</p>\n".format(request.form["field3"])
        try:
            state = str(request.form["field4"])
        except:
            errors += "<p>{!r} is not a valid state.</p>\n".format(request.form["field4"])
        try:
            product = str(request.form["field5"])
        except:
            errors += "<p>{!r} is not a valid product.</p>\n".format(request.form["field5"])
        try:
            year = int(request.form["field6"])
        except:
            errors += "<p>{!r} is not a valid year.</p>\n".format(request.form["field6"])
        try:
            desc = str(request.form["field7"])
        except:
            errors += "<p>{!r} is not a valid description.</p>\n".format(request.form["field7"])
        try:
            pics = int(request.form["field8"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["field8"])

        if pics is not None and name is not None and lat is not None and lon is not None and state is not None and product is not None and year is not None and desc is not None:
            categ = request.form["category"]


            data = {"pics": pics,
                    "name": name,
                    "lat": lat,
                    "lon": lon,
                    "state": state,
                    "product": product,
                    "year": year,
                    "desc": desc,
                    "category": categ
                    }
            prj = Project(data)
            prj_list = ProjectList()
            prj_list.add_project(prj)

            project_all = os.path.join(THIS_FOLDER2, 'static/projects.txt')
            with open(project_all, "r") as read_all:
                project_all = json.load(read_all)
            project_detail = os.path.join(THIS_FOLDER, 'static/projectdetails/project' + str(project_all["data"][-1]["monument_id"]) + '.txt')
            with open(project_detail, "r") as read_details:
                project_details = json.load(read_details)

            folder_name = str(project_details["data"]["monument_id"]) + '_' + project_details["data"]["site_name"]
            dir_name = my_file + folder_name
            UPLOAD_FOLDER = os.path.join(my_file, dir_name)
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            if 'file' not in request.files:
                errors += "<p>{!r} has no file.</p>\n"
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                errors += "<p>{!r} has no selected file.</p>\n"
                return redirect(request.url)
            if file and allowed_file(file.filename):
                try:
                    # Create target Directory
                    os.mkdir(dir_name)
                except FileExistsError:
                    errors += "<p>Directory already exists</p>\n"


                file_loc = "/" + project_details["data"]["site_name"] + '_'
                pics = int(project_details["data"]["transboundary"])
                pic_name = ""
                for x in range(pics):
                    pic_name = file_loc + str(x)
                    pic_loc = os.path.join(UPLOAD_FOLDER, pic_name)
                    if os.path.isfile(pic_loc):
                        continue
                    else:
                        pic_name = project_details["data"]["site_name"] + '_' + str(x) + ".jpg"
                        break
                file.save(os.path.join(UPLOAD_FOLDER, pic_name))

                url = "https://benninisalongo.pythonanywhere.com/static/picturesjpeg/" + folder_name + "/" + pic_name

                change_pics(url, project_details["data"]["monument_id"])






            return '''
                <html>
                    <body>
                        <p>Your project has been added to the database</p>
                        <p><a href="/">Or click here to add another project</a>
                    </body>
                </html>
            '''

    return '''
        <html>
            <body>
                {errors}
                <p>Enter the following data:</p>
                <form method="post" action="." enctype=multipart/form-data>
                    <p><input name="field1" /> Project Name</p>
                    <p><input name="field2" /> Latitude</p>
                    <p><input name="field3" /> Longitude</p>
                    <p><input name="field4" /> State</p>
                    <p><input name="field5" /> Product Type</p>
                    <p><input name="field6" /> Year</p>
                    <p><input style="height:100px" name="field7" /> Description</p>
                    <p><input name="field8" /> Number of Pictures</p>
                    <p>Add pictures (only files ending in .jpg will work): </p>
                    <input type=file name=file>
                    <p></p>
                    <input type="radio" name="category" value="Rockfall"> Rockfall<br>
                    <input type="radio" name="category" value="Slope"> Slope<br>
                    <input type="radio" name="category" value="Smartbox"> Smartbox<br>
                    <input type="radio" name="category" value="Corrosion"> Corrosion
                    <p><input type="submit" value="Add project" /></p>
                </form>

            </body>
        </html>
    '''.format(errors=errors)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()