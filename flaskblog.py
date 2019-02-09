from flask import Flask, render_template
app = Flask(__name__)

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

if __name__ == "__main__" :
	app.run(debug=True)