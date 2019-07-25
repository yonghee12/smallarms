import os
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename

import hcc_main as hcc
import api_func
# import hcc_contents as cr

UPLOAD_FOLDER = './user_upload'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
api = Api(app)
app.secret_key = "secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class YoutubeDescription(Resource):
    def get(self):
        # return api_func.get_descriptions(url)
        # print('\n', request.args)
        urls = request.args.getlist('url')
        data = api_func.get_descriptions(urls)
        data = jsonify(data)
        return data

api.add_resource(YoutubeDescription, '/youtube-description')

@app.route("/")
def root():
	return redirect(url_for('report'))

@app.route("/report", methods=['GET', 'POST'])
def report():
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
			week = request.form.get('week')
			day = filename[-11:-5]
			print('DAY1:', day)
			print("FILENAME:", filename)
			
			if "Reward" in filename:
				print('rw')
				filename = "report.xlsx"
				print('DAY2:', day)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				return redirect(url_for('run_hcc', day=day, medium='rw'), code=301)
			elif "Youtube" in filename:
				print('yt')
				filename = "report.xlsx"
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				print('DAY2:', day)
				return redirect(url_for('run_hcc', day=day, medium='yt', week=week), code=301)
			elif "Instagram" in filename:
				print('ig')
				filename = "report.xlsx"
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				print('DAY2:', day)
				return redirect(url_for('run_hcc', day=day, medium='ig', week=week), code=301)
			elif "Facebook" in filename:
				print('fb')
				filename = "report.xlsx"
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				print('DAY2:', day)
				return redirect(url_for('run_hcc', day=day, medium='fb', week=week), code=301)
			elif "Dive" in filename:
				print('dive')
				filename = "report.xlsx"
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				print('DAY2:', day)
				return redirect(url_for('run_hcc', day=day, medium='dive', week=week), code=301)

	return render_template('report.html', page_title="hcc_rewards")

@app.route("/report_result", methods=['GET'])
def run_hcc():
	week = request.args.get('week')
	medium = request.args.get('medium')
	day = request.args.get('day')
	print('RUN_HCC', day, medium)
	print("DAY3:", day)
	return render_template('report_result.html', hcc=hcc, day=day, medium=medium, week=week)

# @app.route("/test", methods=['GET', 'POST'])
# def test():
# 	return render_template('reward_v1.html', page_title="hcc_rewards", DAY=DAY)

if __name__ == "__main__":
	app.run(debug=True)