import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import hcc_reward as hr

DAY = "1"
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
	return redirect(url_for('report'))

@app.route("/report", methods=['GET', 'POST'])
def report():
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
			day = filename[-11:-5]
			print("DAY0:", filename, DAY, day)
			filename = "rw_report.xlsx"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			# return redirect(url_for('upload_file', filename=filename))
			print("DAY1:", DAY, day)
			return redirect(url_for('run_hr', day=day), code=301)
	return render_template('report.html', page_title="hcc_rewards")

@app.route("/report_result/<day>", methods=['GET'])
def run_hr(day):
	global DAY
	print("DAY2:", DAY)
	print("DAY3:", day)
	DAY = day
	return render_template('report_result.html', hr=hr, DAY=DAY)


# @app.route("/test", methods=['GET', 'POST'])
# def test():
# 	return render_template('reward_v1.html', page_title="hcc_rewards", DAY=DAY)

if __name__ == "__main__":
	app.run(debug=True)