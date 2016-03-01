#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request, render_template

import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: appication/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          
# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    return flask.redirect(flask.url_for('static', filename="index.html"))


@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    '''update the entities via this interface'''
    data = flask_post_json()
    if request.method == 'POST' or request.method == 'PUT':
        newdata = {}
        newdata['x'] = data['x']
        newdata['y'] = data['y']
        counter=0
        data = newdata #all other information is not needed
        with open('world','r') as f:
            cWorld = f.read()
            cWorld.split(':')
            counter = len(cWorld)/24 #3perobject*8bytes
        newdata = {}
        newdata[counter] = data
        counter+=1
        with open('world','a') as f:
            f.write(str(newdata))
    myWorld.update(entity,counter,data)
    return entity  

@app.route("/world", methods=['POST','GET'])    
def world():
    '''you should probably return the world here'''
    if request.method=='GET':
        with open('world','r') as f:
            newWorld = f.read()
            newWorld = newWorld.split('}{')
            for dot in newWorld:
                myWorld.update('world',newWorld[0],newWorld[1])
    return flask.json.jsonify(myWorld.world())

@app.route("/entity/<entity>")    
def get_entity(entity):
    return flask.json.jsonify(myWorld.get(entity))

@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    f = open('world','w')
    f.write("")
    myWorld.clear()
    return None

if __name__ == "__main__":
    app.run()
