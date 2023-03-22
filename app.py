from sudoku import solve
from flask import request
import json
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output)
    y = solve(output)
    print(y)
    x = {"answer": []}
    x['answer'] += y
    print(x)
    return x


if __name__ == "__main__":
    app.run(debug=True)
