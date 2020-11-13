from flask import Flask, render_template, request, redirect
from datetime import datetime
import string, secrets
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///urls.db"

db = SQLAlchemy(app)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(4), unique=True)
    original_url = db.Column(db.String(600))
    date_added = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #Call function to generate 4 character short URL
        self.short_url = self.generate_short_url()
    
    def generate_short_url(self, base=62):
        """
        Uses base62 encoder to shorten id of entry.
        If returned short_url is less than required length of 4
        random characters are chosen from the alpha string.
        """
        records = self.query.all()

        if records:
            last_record = records[-1]
            val = (last_record.id)+1
        else:
            val = 1
        
        alpha = string.digits+string.ascii_letters
        short_url = ""
        while val > 0:
            r = val%base
            short_url += alpha[r]
            val = val//base
        
        #Check if url already exists in db
        link = self.query.filter_by(short_url=short_url).first()

        if link:
            self.generate_short_url()

        if len(short_url) > 4:
            if self.query.filter_by(short_url=short_url[:4]).first():
                self.generate_short_url()

            return short_url[:4]
        else:
            secGen = secrets.SystemRandom()
            new_short = secGen.choices(alpha, k=4)
            
            if self.query.filter_by(short_url=''.join(new_short)).first():
                return self.generate_short_url()

            return ''.join(new_short)
        
        return short_url

@app.route('/')
def index():
    return render_template("index.html")

#Add entered link to db
@app.route('/add_link', methods=['POST'])
def add_link():
    original_url = request.form['original_url']

    link = Link(original_url=original_url)

    db.session.add(link)
    db.session.commit()

    return render_template("link_added.html", new_link=link.short_url)

#Redirect short url to original url
@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first()
    return redirect(link.original_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)