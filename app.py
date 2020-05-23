from PIL import Image, ImageDraw, ImageFont
import os
import os.path
from flask import *
from werkzeug.utils import secure_filename
import time
import string
import random

# UPLOAD_FOLDER = "/home/ubuntu/AssignmentX/uploads/"
UPLOAD_FOLDER = "/home/ubuntu/AssignmentX/uploads/"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "ipynb", "ttf"}


class AssignmentX:
    directoryName = None
    name = None
    opacity = 255
    color1 = (0, 0, 0, 255)
    color2 = (255, 255, 255, 255)
    opage = None
    wtext = None
    sfont = None

    @staticmethod
    def assignmentx(path, path1):

        font = list()
        if AssignmentX.opage == None or AssignmentX.opage == "ucoe":
            SheetImage = "/home/ubuntu/AssignmentX/uploads/essentials/UCoE.jpg"
            fontsize = 75
        else:
            SheetImage = "/home/ubuntu/AssignmentX/uploads/essentials/normal.jpeg"
            fontsize = 100

        if AssignmentX.wtext == None or AssignmentX.wtext == "":
            for files in os.listdir(path):
                if files.endswith(".txt"):
                    TextFile = os.path.join(path, files)
            fileopen = open(TextFile, encoding="utf8")
            text = fileopen.read()
            fileopen.close()
        else:
            text = AssignmentX.wtext
        print(AssignmentX.sfont)
        if AssignmentX.sfont == "no" or AssignmentX.sfont == None:
            font.append(
                ImageFont.truetype(
                    "/home/ubuntu/AssignmentX/uploads/essentials/Utsav-1.ttf",
                    fontsize,
                )
            )
            font.append(
                ImageFont.truetype(
                    "/home/ubuntu/AssignmentX/uploads/essentials/Utsav-2.ttf",
                    fontsize,
                )
            )
            font.append(
                ImageFont.truetype(
                    "/home/ubuntu/AssignmentX/uploads/essentials/Utsav-3.ttf",
                    fontsize,
                )
            )
        else:
            for files in os.listdir(path):
                if files.endswith(".ttf"):
                    font.append(ImageFont.truetype(os.path.join(path, files), fontsize))

        images = list()

        pages = 0
        boolean = 1
        # from numpy import random
        # Opening the blank page
        def type_pages(pages, text, boolean):

            page = Image.open(SheetImage).convert("RGBA")
            width, height = page.size
            if AssignmentX.opage == None or AssignmentX.opage == "ucoe":
                left_margin = 260  #  440
                top_margin = 230  #  325
                line_space = 67  #  96
                bottom_margin = height - 100  # height - 100

            else:
                left_margin = 440
                top_margin = 335
                line_space = 96
                bottom_margin = height - 300

            txt = Image.new("RGBA", page.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt)
            lwidth = 0

            for index, letter in enumerate(text):
                # if top_margin > height - 300:
                #     copy.save("{}{}.png".format(name, pages))
                #     print("PRINTED PAGE {}".format(pages + 1))
                #     pages += 1
                #     text = text[index:]
                #     type_pages(pages, text, boolean)
                #     break

                # print(top_margin, height)
                if (letter == "\n") or (lwidth >= (width - left_margin - 90)):
                    # start_index = index
                    lwidth = 0
                    top_margin += line_space
                    if top_margin > height - 300:
                        txt = Image.alpha_composite(page, txt)
                        # txt.save("{}{}.png".format("name", pages))
                        images.append(txt.convert("RGB"))
                        pages += 1
                        text = text[index:]
                        type_pages(pages, text, boolean)
                        break
                if letter == "\t":
                    lwidth += 100
                human = random.randint(0, 5)
                fonts = random.choice(font)
                add_sub = random.randint(0, 1)

                if letter == "$" and boolean == 1:
                    color = AssignmentX.color2
                    boolean = 0
                    if index == len(text) - 1:
                        # print("DONE WRITING")
                        txt = Image.alpha_composite(page, txt)
                        # txt.save("{}{}.png".format("name", pages))
                        images.append(txt.convert("RGB"))
                        images[0].save(
                            "{}.pdf".format(
                                os.path.join(path1, AssignmentX.directoryName)
                            ),
                            save_all=True,
                            append_images=images[1:],
                        )
                    else:
                        continue
                elif letter == "$" and boolean == 0:
                    color = AssignmentX.color1
                    boolean = 1
                    # if index == len(text) - 1:
                    #     # print("DONE WRITING")
                    #     txt = Image.alpha_composite(page, txt)
                    #     # txt.save("{}{}.png".format("name", pages))
                    #     images.append(txt.convert("RGB"))
                    #     images[0].save(
                    #         "{}.pdf".format(
                    #             os.path.join(path1, AssignmentX.directoryName)
                    #         ),
                    #         save_all=True,
                    #         append_images=images[1:],
                    #     # )
                    # else:
                    #     continue
                elif boolean == 0:
                    color = AssignmentX.color2
                else:
                    color = AssignmentX.color1
                    boolean = 1

                if add_sub == 0:
                    draw.text(
                        (left_margin + lwidth, top_margin + human),
                        letter,
                        # fill=(10, 15, 85, 255),
                        fill=color,
                        font=fonts,
                    )
                else:
                    draw.text(
                        (left_margin + lwidth, top_margin - human),
                        letter,
                        # fill=(10, 15, 85, 255),
                        fill=color,
                        font=fonts,
                    )
                # txt = Image.alpha_composite(page, txt)
                lwidth += draw.textsize(letter, fonts)[0]
                # print(draw.textsize(letter, fonts)[0])
                # print(index)
                if index == len(text) - 1:
                    # print("DONE WRITING")
                    txt = Image.alpha_composite(page, txt)
                    # txt.save("{}{}.png".format("name", pages))
                    images.append(txt.convert("RGB"))
                    images[0].save(
                        "{}.pdf".format(os.path.join(path1, AssignmentX.directoryName)),
                        save_all=True,
                        append_images=images[1:],
                    )
                    # exit()
            # copy.save("text{}.png".format(pages))

        type_pages(pages, text, boolean)


# new instance of flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# index routing
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        AssignmentX.name = request.form["name"]
        AssignmentX.opacity = int(request.form["opacity"])
        lol = request.form["color1"]
        h = lol.lstrip("#")
        a = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
        a = a + (AssignmentX.opacity,)
        AssignmentX.color1 = a
        lol2 = request.form["color2"]
        h2 = lol2.lstrip("#")
        a2 = tuple(int(h2[i : i + 2], 16) for i in (0, 2, 4))
        a2 = a2 + (AssignmentX.opacity,)
        AssignmentX.color2 = a2
        AssignmentX.wtext = request.form["textarea"]
        AssignmentX.opage = request.form["opage"]
        AssignmentX.sfont = request.form["sfont"]
        # print(name)
        # check if the post request has the file part
        N = 2
        # directoryName = time.strftime("%Y%m%d-%H%M%S")
        directoryName = time.strftime("%Y%m%d-%H%M%S").join(
            random.choices(string.ascii_uppercase + string.digits, k=N)
        )
        # directoryName = "lol"
        # parentDir = "C:/Users/Antonio/Desktop/Codes/Kivy/"
        global path
        path = os.path.join(UPLOAD_FOLDER, directoryName)
        os.mkdir(path)
        global path1
        path1 = os.path.join(path, "output")
        os.mkdir(path1)
        # if "file" not in request.files:
        #     flash("No files found")
        #     return redirect(url_for("index.html"))
        # # file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename

        for file in request.files.getlist("file"):
            # if file.filename == "":
            #     flash("No selected file")
            #     return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(path, filename))
        AssignmentX.directoryName = directoryName
        AssignmentX.assignmentx(path, path1)

        return render_template("next.html", name=AssignmentX.name)

        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("index.html")


@app.route("/next.html", methods=["GET", "POST"])
def next():
    return render_template("next.html", name=AssignmentX.name)


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


@app.route("/pptc", methods=["GET", "POST"])
def pptc():
    return render_template("pptc.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


@app.route("/output")
def output():
    # path = "info.xlsx"
    # path = "sample.txt"
    try:
        return send_file(
            "{}.pdf".format(os.path.join(path1, AssignmentX.directoryName)),
            as_attachment=True,
        )
    except:
        return send_file(
            "{}.txt".format("/home/ubuntu/AssignmentX/uploads/essentials/error"),
            as_attachment=True,
        )


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=True)
    except:
        app.run(host="0.0.0.0", debug=True)
