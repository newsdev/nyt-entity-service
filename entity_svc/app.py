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
from fuzzywuzzy import fuzz, process
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

models.database.connect()
models.database.create_tables([models.Entity, models.EntityNote], safe=True)

def create_entity(response):
    """
    Creates and returns an entity.
    """

    user_email = request.environ['jwt_user_email'] or 'test@test.dev'

    e = models.Entity.create(name=response['request']['name'])
    en = models.EntityNote.create(entity=e.id,user_email=user_email)
    response['response']['created'] = True
    response['response']['name'] = e.name
    response['response']['uuid'] = str(e.id)

    print(response)

    return response

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        payload = utils.clean_payload(dict(request.form))

        if not payload.get('name', None):
            return Response('bad request', 400)

        lookup = dict([(e.name, e.id) for e in models.Entity.select()])
        entity_list = list(lookup.keys())

        name = payload['name']
        score = 0

        print(entity_list)

        if len(entity_list) > 0:
            name, score = process.extractOne(payload['name'], entity_list)

        response = {}
        response['request'] = {}
        response['request']['name'] = payload['name']
        response['request']['create_if_below'] = payload.get('create_if_below', settings.MINIMUM_SCORE)
        response['response'] = {}
        response['response']['score'] = score

        if payload.get('create_if_below', None):
            if score < int(payload['create_if_below']):
                response = create_entity(response)
                return jsonify(response)

        if score < settings.MINIMUM_SCORE:
            response = create_entity(response)
            return jsonify(response)

        response['response']['created'] = False
        response['response']['name'] = name
        response['response']['uuid'] = lookup[name]

        return jsonify(response)

    user_email = request.environ['jwt_user_email'] or 'test@test.dev'
    return Response(user_email, 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008, debug=True)
