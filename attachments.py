#!/usr/bin/env python
__author__ = 'Michael Rosata mrosata1984@gmail.com'
__package__ = ''

import os
import random
import string
import pprint
from datetime import datetime

from werkzeug.utils import secure_filename as werkzeug_secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
FILENAME_MAXLENGTH = 32

if __name__ == '__main__':
    """Tests Go Here"""
else:
    class attach:
        def __init__(self, app, request):
            """
            Set up the attach object to upload files, probably should be
            doing some sort of instanceof here.
            :param app:
            :type app:
            :param request:
            :type request:
            :return:
            :rtype:
            """
            self.app = app
            self.request = request
            self.base = os.path.abspath(os.path.join(app.root_path,
                                        self.app.config['UPLOAD_FOLDER']))
            self.upload_dir = self.get_upload_directory()

        def attach(self, post_name):
            self.post_name = post_name
            try:
                return self.upload_file()
            except IOError, error:
                print error
                return False

        def upload_file(self):
            """ Get the file from the POST request and pass it to the other 
            class methods to check and prep it, then save it local and return
            path to saved file
            :return:
            :rtype:
            """
            if self.request.method == 'POST':
                _file = self.request.files[self.post_name]
                if _file and file_allowed(_file.filename):
                    # File extension is allowable, so try to save it and any
                    # exception raised will be caught by self.attach()
                    if not self.upload_dir:
                        raise IOError('could not resolve dir')
                    filename = secure_filename(_file.filename)
                    image_path = os.path.join(self.upload_dir, filename)
                    _file.save(image_path)
                    # If no exception was raised, we return the image_path
                    return image_path.lstrip(self.base)
                else:
                    # There was no file, or the file is not acceptable ext
                    return False
        
        def get_upload_directory(self):
            """Figures out upload directory based on app config and also the
            current year and month. Creates later folders if not exists
            :return:
            :rtype:
            """
            base = self.base
            year = str(datetime.utcnow().year)
            month = str(datetime.utcnow().month)
            full_path = os.path.join(base, year, month)
            if not os.path.isdir(full_path):
                try:
                    if not os.path.isdir(os.path.join(base, year)):
                        os.makedirs(full_path)
                    else:
                        os.mkdir(full_path)
                except OSError:
                    return False
            return full_path


def secure_filename(filename):
    """
    This function calls werkzeugs function after first making the
    filename unique for our own needs.
    :param filename:
    :type filename:
    :return:
    :rtype:
    """
    base = filename.rsplit('.', 1)[0]
    ext = filename.rsplit('.', 1)[1]
    uid = ''.join(random.choice(string.lowercase) for i in range(32))
    # Concatenate file bits and keep filename under 32
    slice_ind = FILENAME_MAXLENGTH - (len(ext) + 1)
    if len(base) > 16:
        base = base[:16]
    filename = (base + uid)[:slice_ind] + '.' + ext
    return werkzeug_secure_filename(filename)


def file_allowed(filename):
    """Returns bool of whether filename fits allowed extensions based on const
    with name ALLOWED_EXTENSIONS
    :param filename:
    :type filename:
    :return:
    :rtype:
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS