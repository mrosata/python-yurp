import os
import pprint
from datetime import datetime
from flask import Flask, render_template, url_for, request,\
    redirect, flash, send_from_directory, send_file
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from database_setup import Entry, Label, Day, Attachment, CategoryLink, Base
from attachments import attach
from parsed_entry import Parsed_Entry

dump = pprint.PrettyPrinter(depth=8,indent=4)

engine = create_engine('sqlite:///yurp.application.db')
# Initial the application and create db session object
app = Flask(__name__)
DBSession = sessionmaker(bind=engine)
session = DBSession()


# All Routing for Yurp Entry Web Application
@app.route('/')
def main_page():
    entries = get_entries()
    return render_template('_main.html', entries=entries)


@app.route('/archive/')
def archive_page():
    entries = get_entries()
    categories = session.query(Label).filter_by(type='category').all()
    return render_template('_archive.html',
                           entries=entries, categories=categories)


@app.route('/entry/<int:entry_id>')
def entry_page(entry_id):
    try:
        entry = session.query(Entry).filter_by(id=entry_id).first()
        entry = Parsed_Entry(entry, session.query)
        return render_template('_entry.html', entry=entry)
    except AttributeError:
        return render_template('_404.html')


@app.route('/contact/')
def contact_page():
    return render_template('_contact.html')


# Static Uploads, Attachments for entries.
@app.route('/uploadss/<year>/<month>/<file>')
def serve_attachment(year, month, file):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'],
                                           year, month), file)


# Hybrid Pages, pages that both display and have alternative POST functionality

@app.route('/create/entry/', methods=['GET', 'POST'])
def new_page():
    if request.method == 'POST':
        # Check that we have all the required info
        for val in ['author', 'title', 'content', 'category', 'publicity']:
            # Make sure that the required fields have been filled out.
            if (not (val in request.form)) or request.form[val] == '':
                flash('Form was not filled out properly')
                return render_template('_main.html')

        author = int(request.form['author'])
        title = request.form['title']
        content = request.form['content']
        gist = request.form['gist']
        category = int(request.form['category'])
        publicity = request.form['publicity']
        new_id = insert_entry(author, title, content, gist, category, publicity)
        save_label_link(new_id, category)
        # Check if there was an image sent with the entry form as well.
        upload_handler = attach(app, request)
        saved_file = upload_handler.attach('image')
        if saved_file:
            insert_attachment(saved_file, new_id, 'image')

        flash('Inserted new Entry')

    # Regardless of request.method, we will render the new entry page
    categories = session.query(Label).filter_by(type='category').all()
    return render_template('_new.html', categories=categories)


@app.route('/edit/entry/<int:entry_id>/', methods=['GET', 'POST'])
def edit_page(entry_id):
    if request.method == 'POST':
        # Check that we have all the required info
        for val in ['author', 'title', 'content', 'category', 'publicity']:
            # Make sure that the required fields have been filled out.
            if (not (val in request.form)) or request.form[val] == '':
                flash('Form was not filled out properly')
                return render_template('_main.html')

        author = int(request.form['author'])
        title = request.form['title']
        content = request.form['content']
        gist = request.form['gist']
        category = int(request.form['category'])
        publicity = request.form['publicity']
        save_label_link(entry_id, category)
        update_entry(entry_id, author, title, content,
                     gist, category, publicity)
        # Check if there was an image sent with the entry form as well.
        upload_handler = attach(app, request)
        saved_file = upload_handler.attach('image')
        if saved_file:
            update_attachment(saved_file, entry_id, 'image')
        flash('Edited the Entry')

    # Regardless of request.method, we will render the edit entry page
    categories = session.query(Label).filter_by(type='category').all()
    # Need to get the entry for this page
    entry = get_entry(entry_id)
    return render_template('_edit.html',
                           categories=categories, entry=entry)


@app.route('/create/label/category', methods=['POST'])
def create_category():
    if request.form['newCategory'] and request.form['newCategory'] is not '':
        name = request.form['newCategory']
        message = insert_label('category', name)
        flash(message, 'Category')
    else:
        flash('Sorry, You didn\'t fill out the form correctly!')
    return redirect(request.referrer)


# CRUD Functionality (Create, Delete)
def insert_label(_type, name):
    label = Label(type=_type, name=name)
    session.add(label)
    session.commit()
    return 'successfully inserted category %s!' % name


def insert_entry(author, title, content, gist, category, publicity):
    entry = Entry(author=author, title=title, gist=gist,\
                  content=content, category=category, publicity=publicity)
    session.add(entry)
    session.commit()
    return entry.id


def update_entry(id, author, title, content, gist, category, publicity):
    the_time = datetime.utcnow()
    entry = session.query(Entry).filter_by(id=id).\
        update({Entry.author: author, Entry.title: title, Entry.gist: gist,
               Entry.content: content, Entry.category: category,
               Entry.publicity: publicity, Entry.last_edit: the_time})
    session.commit()
    return entry


def insert_attachment(src, entry_id, _type):
    attachment = Attachment(src=src, entry_id=entry_id, type=_type)
    session.add(attachment)
    session.commit()
    return attachment.id


# TODO: Delete the old uploaded file
def update_attachment(src, entry_id, _type):
    attachment = session.query(Attachment).filter_by(entry_id=entry_id).\
        update({Attachment.src: src, Attachment.entry_id: entry_id,
                Attachment.type: _type})
    session.commit()
    return attachment


def delete_entry(id):
    pass


def save_label_link(entry_id, label_id):
    new_link = CategoryLink(label_id=label_id, entry_id=entry_id)
    session.add(new_link)
    session.commit()
    return new_link.id


# Functions for returning data from db for use in app.

def get_entries(limit=12):
    raw_entries = session.query(Entry).limit(limit)
    entries = []
    for entry in raw_entries:
        entry = Parsed_Entry(entry, session.query)
        entries.append(entry)
    return entries


def get_entry(id):
    id = int(id)
    entry = session.query(Entry).filter_by(id=id).first()
    entry = Parsed_Entry(entry, session.query)
    return entry


running_on_python_anywhere = False

# Make sure to keep the uploads directory name relative
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'ZaR%tC3SzAw48vm2./2!'

if not running_on_python_anywhere and __name__ == '__main__':
    app.debug = True
    app.run()