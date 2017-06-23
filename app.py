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
from pyiap.pyiap_flask_middleware import VerifyJWTMiddleware
import requests

import models
import utils

settings = importlib.import_module('config.%s.settings' % utils.get_env())
app = Flask(__name__, template_folder=settings.TEMPLATE_PATH)
# app.wsgi_app = VerifyJWTMiddleware(app.wsgi_app)
app.debug=settings.DEBUG

@app.before_request
def _db_connect():
    models.database.connect()

# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not models.database.is_closed():
        models.database.close()

models.database.connect()
models.database.create_tables([models.Entity, models.EntityNote], safe=True)
models.database.close()

def create_entity(response):
    """
    Creates and returns an entity.
    """

    user_email = request.environ.get('HTTP_X_GOOG_AUTHENTICATED_USER_EMAIL', None) or 'test@test.dev'

    e = models.Entity.create(name=response['request']['name'],user_email=user_email)
    en = models.EntityNote.create(entity=e.id,user_email=user_email,note="Created by script.")

    response['response']['created'] = True
    response['response']['name'] = e.name
    response['response']['uuid'] = str(e.id)

    return response

@app.route('/healthcheck', methods=['GET'])
def health():
    return Response('ok')

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':

        context = utils.build_context(request)
        page = utils.get_page(request)

        all_entities = models.Entity.select()\
                            .where(models.Entity.active == True)\
                            .where(models.Entity.canonical_entity >> None)

        context['entities'] = all_entities\
                            .order_by(models.Entity.created.desc())\
                            .paginate(page, settings.ITEMS_PER_PAGE)

        context = utils.paginate(request, all_entities.count(), page, context)

        return render_template('entity_list.html', **context)

    if request.method == 'POST':
        payload = utils.clean_payload(dict(request.form))

        if not payload.get('name', None):
            return Response('bad request', 400)

        lookup = dict([(e.name, e.id) for e in models.Entity.select()])
        entity_list = list(lookup.keys())

        name = payload['name']
        score = 0

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

@app.route('/entity/set/canonical/', methods=['POST'])
def set_canonical_entity():
    if request.method == "POST":
        payload = utils.clean_payload(dict(request.form))
        print("Payload: ", payload)

        if payload.get('entity', None) and payload.get('canonical_entity', None):
            if utils.valid_uuid(payload['entity']) and utils.valid_uuid(payload['canonical_entity']):
                # If payload['entity'] == payload['canonical_entity'],
                # then the user moved an entity back to where it was originally
                # placed on the page. This could signify the user rectifying
                # a mistake in placement.
                if payload['entity'] == payload['canonical_entity']:
                    e = models.Entity\
                            .update(canonical_entity=None)\
                            .where(models.Entity.id==payload['entity'])
                    e.execute()
                    return(jsonify({"entity": payload['entity'], "canonical_entity": None}))
                else:
                    e = models.Entity\
                                .update(canonical_entity=payload['canonical_entity'])\
                                .where(models.Entity.id==payload['entity'])
                    e.execute()
                    return(jsonify({"entity": payload['entity'], "canonical_entity": payload['canonical_entity']}))

            return Response('bad request', 400)
        return Response('bad request', 400)
    return Response('bad request', 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
