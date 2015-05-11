#!/usr/bin/env python
__author__ = 'Michael Rosata mrosata1984@gmail.com'
__package__ = ''

from flask import Markup

from database_setup import Label, Attachment


class Parsed_Entry:

    def __init__(self, db_entry, query):
        self.db_entry = db_entry
        self.query = query

        self.id = db_entry.id
        self.title = Markup(db_entry.title)
        self.author = db_entry.author
        self.content = Markup(db_entry.content)
        self.gist = db_entry.gist
        self.inserted = db_entry.inserted

        self.image = self.check_attachments()
        self.category = self.check_label('category')

    def check_attachments(self, _type='image'):
        attachment = self.query(Attachment).\
            filter_by(entry_id=self.id, type=_type).first()
        ret_attach = {'id':0, 'type': '', 'src': ''}
        if attachment:
            ret_attach['id'] = attachment.id
            ret_attach['type'] = attachment.type
            ret_attach['src'] = str(attachment.src).lstrip('/')
            ret_attach['year'] = attachment.src.split('/')[0]
            ret_attach['month'] = attachment.src.split('/')[1]
            ret_attach['file'] = attachment.src.split('/')[2]
            return ret_attach
        return ''

    def check_label(self, _type='category'):
        label = self.query(Label).\
            filter_by(id=self.db_entry.category, type=_type).one()
        ret_label = {'id': 0, 'name': ''}
        if label:
            try:
                ret_label['name'] = label.name
                ret_label['id'] = label.id
            except AttributeError, e:
                print e
        return ret_label