from flask import Flask, render_template
from neoscore.common import *
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/open_neoscore')
def open_neoscore():
    neoscore.setup()
    Text(ORIGIN, None, "Hello, neoscore!")
    neoscore.show()
    return 'Neoscore document/window opened successfully!'

if __name__ == '__main__':
    app.run(debug=True)