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
import webapp2
import hmac

from google.appengine.ext import db

secret = "suvobhikari"

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

class MainHandler(Handler): 
    def get(self):
        self.response.headers['Content-Type']="text/plain"
        visit_cookie = self.request.cookies.get('visits',None)
        cookie_valid = False
        if "|" in visit_cookie:
        	cookie_valid=True
        
        if visit_cookie and cookie_valid:
        	v = visit_cookie.split("|")
        	visits = v[0]
        	if hmac.new(secret, visits).hexdigest() == v[1]:
        		#cookie is valid
        		visits = int(visits)+1
        	else:
        		visits=0
        else:
        	visits=0

        new_cookie = str(visits)+"|" + hmac.new(secret, str(visits)).hexdigest()
        self.response.headers.add_header('Set-Cookie', "visits= %s" % new_cookie)
        if visits>1000000:
        	self.write("You are the best")		
        else:	
        	self.write("You have been here %s times" % visits)		


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)



# class SignupHandler(Handler):
# 	def get(self):
# 		self.render("signup.html")

# class WelcomeHandler(Handler):
# 	def get(self):
# 		self.render("signup.html")

#, ('/signup', SignupHandler), ('/welcome', WelcomeHandler)