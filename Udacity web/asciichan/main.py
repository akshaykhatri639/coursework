#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
import os
import jinja2
import urllib2
from xml.dom import minidom
import webapp2
from google.appengine.ext import db
import sys
sys.path.insert(0, 'libs')

IP = "http://api.hostip.info/?ip="
GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"

def gmaps_img(points):
    ###Your code here
    s = GMAPS_URL
    i=len(points)
    j=0
    for p in points:
        if j==i-1:
            s = s + "markers=" + str(p.lat) + "," + str(p.lon)
        else:
            s = s + "markers=" + str(p.lat) + "," + str(p.lon) +"&" 
        j+=1
    return s

def find_coords(ip):
    ip2="4.2.2.2"
    ip2="27.4.149.22"
    content =None
    try:
        content = urllib2.urlopen(IP + ip2).read()
    except URLError:
        return

    if content:
        x = minidom.parseString(content)
        y = x.getElementsByTagName("gml:coordinates")[0].childNodes
        z=y[0].nodeValue
        aa= z.split(",")
        return db.GeoPt(aa[1], aa[0])


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Art(db.Model):
    title = db.StringProperty(required = True)
    art=db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty(required=False)

class MainHandler(Handler): 
    def render_front(self, title="",art="",error=""):
        arts = db.GqlQuery("select * from Art order by created desc")
        arts = list(arts)
        points=[]
        for a in arts:
            if a.coords:
                points.append(a.coords)

        img_url = None
        if points:
            img_url = gmaps_img(points)
        self.render("front.html", title=title,art=art,error=error, arts = arts, img_url=img_url)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if art and title:
            coords = find_coords(self.request.remote_addr)
            a = Art(title=title,art=art, coords= coords)
            a.put()
            self.redirect("/")

        else:
            error = "We need both title and art!"
            self.render("front.html", error=error,title=title,art=art)
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


