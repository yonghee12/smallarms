from flask import Flask, render_template

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import hcc_reward as hr

DAY = ""
UPLOAD_FOLDER = './user_upload'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
app.secret_key = "secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def root():
	return redirect(url_for('reward'))

@app.route("/test", methods=['GET', 'POST'])
def test():
	global DAY
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
			filename = secure_filename(file.filename)
			DAY = filename[-11:-5]
			print(filename, DAY)
			filename = "rw_report.xlsx"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# return redirect(url_for('upload_file', filename=filename))
			return redirect(url_for('run_hr'))
	return render_template('reward_v1.html', page_title="hcc_rewards", DAY=DAY)

@app.route("/reward_result", methods=['GET', 'POST'])
def run_hr():
	global DAY
	print(DAY)
	return render_template('reward_result.html', hr=hr, DAY=DAY)

@app.route("/reward", methods=['GET', 'POST'])
def reward():
	global DAY
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
			filename = secure_filename(file.filename)
			DAY = filename[-11:-5]
			print(filename, DAY)
			filename = "rw_report.xlsx"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# return redirect(url_for('upload_file', filename=filename))
			return redirect(url_for('run_hr'))
	# return render_template('hcc_daily_rewards.html', page_title="hcc_rewards", DAY=DAY)
	return render_template('reward_v2.html', page_title="hcc_rewards", DAY=DAY)
# hr.run("190207")

if __name__ == "__main__":
	app.run(debug=True)

# UPLOAD_FOLDER