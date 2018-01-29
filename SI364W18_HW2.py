## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album = StringField('Enter the name of an album:', validators=[Required()])
	rating = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1','1'),('2','2'),('3','3')], validators=[Required()])
	submit = SubmitField('Submit')


####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


@app.route('/artistform')
def see_artist_form():
	return render_template('artistform.html')

@app.route('/artistinfo')
def see_artist_info():
	if request.method == 'GET':
		artist = request.args.get('artist','')
		itunes_data = requests.get('https://itunes.apple.com/search?term={}&limit=10&country=us'.format(artist))
		json_data = json.loads(itunes_data.text)
		objects = json_data['results']
		return render_template('artist_info.html', objects= objects)

@app.route('/artistlinks')
def see_artist_links():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist>')
def see_specific_artist(artist):
	artist_data = requests.get('https://itunes.apple.com/search?term={}&limit=10&media=music&entity=musicTrack'.format(artist))
	json_artist_data = json.loads(artist_data.text)
	results = json_artist_data['results']
	return render_template('specific_artist.html', results=results)

@app.route('/album_entry')
def album_form():
	album_form = AlbumEntryForm()
	return render_template('album_entry.html', form=album_form)

@app.route('/album_data', methods=['GET','POST'])
def see_ablum_result():
	form = AlbumEntryForm(request.form)
	if request.method=='POST' and form.validate_on_submit():
		album = form.album.data
		rating = form.rating.data
		album_data = requests.get('https://itunes.apple.com/search?term={}&media=music&entity=album&limit=1'.format(album))
		json_album_data = json.loads(album_data.text)
		results = json_album_data['results'][0]
		return render_template('album_data.html',album=album, rating=rating, results=results)
	flash('All fields are required!')
	return redirect(url_for('album_form'))



if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
