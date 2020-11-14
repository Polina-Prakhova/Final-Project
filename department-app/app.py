from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    lines = [{'name': 'dfasfasf', 'employees': 22, 'salary': 1},
             {'name': 'dfasfasf', 'employees': 22, 'salary': 1},
             {'name': 'dfasfasf', 'employees': 22, 'salary': 1},
             {'name': 'dfasfasf', 'employees': 22, 'salary': 1}]
    return render_template('departments.html', title='Departments',
                           headers=['1', '2', '3'], departments=lines)


if __name__ == "__main__":
    app.run(debug=True)
