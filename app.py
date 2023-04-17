from flask import Flask, render_template, request, make_response, send_file, redirect
from zipfile import ZipFile
import os

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_app', methods=['POST'])
def create_app():
    # Get user choices from form
    db_type = request.form['db_type']
    add_auth = request.form.get('add_auth', False)
    front_end = request.form['front_end']
    app_name = request.form['app_name']

    # Generate Flask app code based on user choices
    app_code = f"""from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '{db_type}:///<your_database_uri>'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

"""
    if add_auth:
        app_code += """login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

"""

    if front_end == 'Bootstrap':
        app_code += """from flask_bootstrap import Bootstrap

bootstrap = Bootstrap(app)

"""

    app_code += f"""@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
"""

    # Save app code to file
    with open(f"{app_name}.py", 'w', encoding='utf-8') as f:
        f.write(app_code)

    # Create a ZIP file containing the app code and HTML file
    zip_name = f"{app_name}.zip"
    with ZipFile(zip_name, 'w') as myzip:
        myzip.write(f"{app_name}.py")
        with myzip.open('templates/index.html', 'w') as f:
            html = f"""
<!DOCTYPE html>
<html>
<head>
	<title>{app_name} - Flask App</title>
</head>
<body>
	<h1>{app_name}</h1>
	<p>Congratulations! You have successfully created a Flask app.</p>
	<p>To run the app:</p>
	<ol>
		<li>Install Flask: <code>pip install flask</code></li>
		<li>Run the app: <code>python {app_name}.py</code></li>
	</ol>
</body>
</html>
"""
            f.write(html.encode('utf-8'))

    # Send the ZIP file for download
    file_path = os.path.join(app.root_path, zip_name)
    response = make_response(send_file(file_path, as_attachment=True))
    response.headers['Content-Disposition'] = f'attachment;'

# Redirect to complete.html
    return redirect('/complete')

@app.route('/complete')
def complete():
    return render_template('complete.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
