from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.fields import FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from flask_bootstrap import Bootstrap
import numpy as np
import scipy.misc
from PIL import Image,ImageColor
import matplotlib.pyplot as plt



# creating the app 
app = Flask(__name__)
app.config['SECRET_KEY'] = "dev"
Bootstrap(app)

# creating the upload form

class Image_form(FlaskForm):
    image = FileField(validators=[FileRequired(message="upload an image to proceed"), FileAllowed(['jpg', 'png', 'jpeg'],message='Images only!')])
    col_num = IntegerField("how many colors do you want to extract")
    submit = SubmitField("submit")

# changes from rgb code to hexcode
def rgb2hex(color):
    return "#{:02x}{:02x}{:02x}".format(color[0],color[1],color[2])

#  checks for shades of a color 
def check_shade(p, list, delta):
    for col in list:
        score = 0
        for c in range(len(col)):
            if col[c]>=p[c]>=col[c]-delta or col[c]<=p[c]<=col[c]+delta:
                score += 1
        if score == len(col):
            return True
    return False
        

            

@app.route("/", methods=["GET","POST"])
def webpage():
    image = Image_form()
    if image.validate_on_submit():
        img = np.array(Image.open(image.image.data))
        pixel=[]
        pixel_shade = []
        # turns the nested array into a list of colors(rgb)
        for i in img:
            for p in i:
                pixel.append(rgb2hex(p))
        # to get the unique colors and the number of their occurrences
        hex_c,count = np.unique(pixel, return_counts=True)
        count_sort_ind = np.argsort(-count)

        hex_common = []
        # to get the colors of different shades that appear in the image
        for  i in hex_c[count_sort_ind].tolist():
            if not check_shade(ImageColor.getrgb(i),pixel_shade,40):
                pixel_shade.append(ImageColor.getrgb(i))
                hex_common.append(i)
        
        # to check if the number of color the user wants to extract from the image can be extracted
        if len(hex_common) > image.col_num.data:
            hex= hex_common[:image.col_num.data]
        else:
            hex=hex_common
        return render_template("index.html",form=image, colors=hex)

    return render_template("index.html",form=image, hex=None)



if __name__ == "__main__":
    app.run(debug=True)
    