'''
A helper wizard for the Sagittarius Online Game Service.
Copyright: (c) 2015 William Gaul
License: MIT, see LICENSE for more details
'''
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(port=8080)



########################################
# GLOBAL CLASSES/METHODS
########################################