from flask import Flask, render_template
app = Flask(__name__)

from application import routes


#@app.route('/')
#def index():
#    title ="Klimaentwicklung"
#    return render_template("index.html", title=title)
#
#
#
#@app.route('/Klimaauswirkung')
#def about():
#    title ="Klimaauswirkung"
#    return render_template("Klimaauswirkung.html", title=title)