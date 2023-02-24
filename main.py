from flask import Flask, request, redirect
from firebase_admin import credentials, firestore, initialize_app
import hashlib
import string
import random

app = Flask(__name__)

cred = credentials.Certificate("./serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

@app.route('/', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    identifier = generate_identifier()
    db.collection('urls').document(identifier).set({
        'original_url': original_url,
        'shortened_url': f'http://127.0.0.1:5000/{identifier}'
    })

    return f'http://127.0.0.1:5000/{identifier}'

@app.route('/<identifier>')
def redirect_to_url(identifier):
    doc_ref = db.collection('urls').document(identifier)
    doc = doc_ref.get()
    print('doc', doc.to_dict())
    if doc.exists:
        original_url = doc.to_dict()['original_url']
        return redirect(original_url)
    else:
        return 'Not found', 404

def generate_identifier():
    chars = string.ascii_letters + string.digits
    identifier = ''.join(random.choices(chars, k=8))


    doc_ref = db.collection('urls').document(identifier)
    doc = doc_ref.get()
    while doc.exists:
        identifier = ''.join(random.choices(chars, k=8))
        doc_ref = db.collection('urls').document(identifier)
        doc = doc_ref.get()
    return identifier

if __name__ == '__main__':
    app.run()