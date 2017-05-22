#!/usr/bin/env python

import argparse
import base64
import csv
import datetime
import glob
import json
import importlib
import io
import os
import re
import time

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from flask import Flask, render_template, request, make_response, Response, redirect, jsonify
import peewee
from peewee import *
from pyiap.flask import VerifyJWTMiddleware
import requests

import models
import utils

settings = importlib.import_module('config.%s.settings' % utils.get_env())
app = Flask(__name__, template_folder=settings.TEMPLATE_PATH)
app.wsgi_app = VerifyJWTMiddleware(app.wsgi_app)
app.debug=settings.DEBUG

def match_request_entity(payload, entity_list):
    """
    Testable unit of business logic for matching an entity.
    """

def create_request_entity(payload):
    """
    Testable unit of business logic for creating an entity.
    """


@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST':
        payload = utils.clean_payload(dict(request.form))

        if not payload['name']:
            return Response('bad request', 400)

        entity_list = models.Entity.select('name')
        m = match_request_entity(payload, entity_list)

        if m:
            return Response(jsonify(m), 200)

        if not m:
            c = create_request_entity(payload)

            if c:
                return Response(jsonify(c), 200)

    return Response('bad request', 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008, debug=True)
