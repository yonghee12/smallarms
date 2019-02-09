from flask import Flask, render_template

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import hcc_reward as hr

UPLOAD_FOLDER = './user_upload'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


posts = [
	{
		'author': '천용희',
		'title': 'Blog Post 1',
		'content' : '첫번째 포스트',
		'date_posted' : 'April 20, 2018'
	},
	{
		'author' : 'John Doe',
		'title' : 'Blog Post 2',
		'content' : '두번째 포스트',
		'date_posted' : 'April 20, 2018'
	}
]

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts)

@app.route("/about")
def about():
	return render_template('about.html', page_title='About')

@app.route("/reward", methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			# filename = secure_filename(file.filename)
			filename = "rw_report.xlsx"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('upload_file',
									filename=filename))
	return render_template('hcc_daily_rewards.html', page_title="hcc_rewards")

@app.route("/reward_result", methods=['GET', 'POST'])
def run_hr():
	return render_template('reward_result.html', hr=hr, print=print)

# hr.run("190207")

if __name__ == "__main__" :
	app.run(debug=True)

# UPLOAD_FOLDER