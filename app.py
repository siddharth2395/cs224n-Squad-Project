from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        context = request.form['context']
        question = request.form['question']
        print context
        print question
        return render_template('index.html')

    else:

        return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0')
