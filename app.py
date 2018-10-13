from flask import (
    Flask, render_template, jsonify, session, request, Response, redirect,
    url_for
)


from flask_wtf import FlaskForm
from wtforms import (
    widgets, StringField, BooleanField, PasswordField,
    SubmitField, RadioField, SelectMultipleField, FormField,
    DecimalField, FloatField, IntegerField, FieldList,
    SelectField, TextField
)

from wtforms.validators import DataRequired
import google.cloud
from google.cloud import texttospeech
from twilio.twiml.voice_response import Play, VoiceResponse
import argparse
import datetime
import pprint
import twilio
import twilio.rest
from twilio.rest import Client
# [START storage_upload_file]
from google.cloud import storage


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

def create_bucket(bucket_name):
    """Creates a new bucket."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created'.format(bucket.name))

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    blob.make_public()

    account_sid = 'AC2aaeb8e0ddde930b515da7858ba847de'
    auth_token = '315c08f39047b97174e2cba3d986ce09'
    client = Client(account_sid, auth_token)
    url = blob.generate_signed_url(
        # This URL is valid for 1 hour
        expiration=datetime.timedelta(hours=0.1),
        # Allow GET requests using this URL.
        method='GET')
    newurl = "?Body="+url
    call = client.calls.create(
                            url='https://handler.twilio.com/twiml/EHb0c94544d1edd57d16459f4dfb0c953b'+newurl,
                            to='+19086352451',
                            from_='+17174708894'
                        )
    print('The signed url for {} is {}'.format(blob.name, url))

    #print(call.sid)
def get_var_value(filename="varstore.dat"):
    with open(filename, "r+") as f:
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val
# [END storage_upload_file]
def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))

def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()
    print('Bucket {} deleted'.format(bucket.name))



@app.route('/')
def textbox_form():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def text():
    print("flag1")
    text = request.form['text']
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    your_counter = get_var_value()
    print(your_counter)
    create_bucket("tryqwerty"+str(your_counter))
    upload_blob("tryqwerty"+str(your_counter), "output.mp3", "output")
    return redirect("/temp")


@app.route('/temp')
def temp():
    return render_template("temp.html")


if __name__ == '__main__':
   app.debug = True
   app.run()
   #delete_blob("plswork", "output")
   #delete_bucket("plswork")
