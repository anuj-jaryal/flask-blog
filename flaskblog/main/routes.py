from flask import  render_template, Blueprint


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home/index.html')

@main.route('/about')
def about():
    return render_template('home/about.html')
