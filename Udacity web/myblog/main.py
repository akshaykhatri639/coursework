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
import random
import string
import hashlib
import json

from google.appengine.ext import db

secret = "suvobhikari"

def make_us_hash(username):
	h = hashlib.sha256(username + secret).hexdigest()
	return "%s|%s" % (username,h)
    

def make_salt():
   return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw,salt=""):
    if salt=="":
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    v = h.split("|")
    if h==make_pw_hash(name, pw,v[1]):
        return True
    return False

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

class Users(db.Model):
	username = db.StringProperty(required= True)
	hash_val = db.StringProperty(required= True)
	email = db.StringProperty(required= False)

class Blogs(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class SignupHandler(Handler):
	def render_signup(self, username="", uerror="", verror="", error="", email=""):
		self.render("signup.html", username=username, uerror=uerror, verror=verror, error=error, email=email)

	def get(self):
		self.render_signup()

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		if username and password and verify:
			c= db.GqlQuery("select * from Users where username= :username" ,username=username)
			if not c.get(): #self.validuser(c,username)
				h = str(make_us_hash(username))
				p = make_pw_hash(username,password)
				u = Users(username=username,hash_val=p,email=email)
				u.put()
				self.response.headers.add_header('Set-Cookie', 'user_id=%s' % h)
				self.redirect("/welcome") 
			
			else:	
				self.render_signup(username=username,uerror="This username already exists",email=email)

		else:
			error = "All fields are essential!"
			self.render_signup(username=username,error=error,email=email)	
    	
class LoginHandler(Handler):
	def validuser(self,c,username):
		for item in c:
				if item.username==username:
					return item.hash_val
					

	def render_login(self,username="",error=""):
		self.render("login.html",username=username,error=error)

	def get(self):
		self.render_login()

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		c = db.GqlQuery("select * from Users")
		g= self.validuser(c,username)
		if g:	
			t = g.split("|")

			if g==make_pw_hash(username,password,t[1]) :
				#data valid
				h = str(make_us_hash(username))
				self.response.headers.add_header('Set-Cookie', 'user_id=%s' % h)
				self.redirect("/welcome") 
			else:
				self.render_login(username=username,error="Invalid Login")
		else:	
			self.render_login(username=username,error="Invalid Login")




class WelcomeHandler(Handler):
	def get(self):
		cook = self.request.cookies.get("user_id")
		t=cook.split("|")
		if str(make_us_hash(t[0]))==str(cook):
			#cookie valid
			self.write("Welcome, " + t[0])
		else:
			self.redirect("/signup")	


class LogoutHandler(Handler):
	def get(self):
		self.response.delete_cookie('user_id')
		self.redirect("/signup")

class PermalinkHandler(Handler):
	def get(self, key):
		key=key[1:]
		k=int(key)
		blog = Blogs.get_by_id(k)
		if not blog:
			self.write("blog not found")
		else:
			self.render("perma.html",blog=blog,h="hello")

class AddpostHandler(Handler):
	def render_form(self,subject="",content="",error=""):
		self.render("newpost.html",subject=subject,content=content,error=error)

	def get(self):
		self.render_form()

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			b = Blogs(subject=subject ,content=content)
			b.put()
			key = b.key()
			k = key.id()
			self.redirect( str(k) )
			
		else:
			error = "subject and content both are essential!"
			self.render_form(subject,content,error)	

class Json(Handler):
	def get(self):
		self.response.headers["Content-Type"] = "application/json"
		# di = {"a":[1], "b":[1,2]}
		# self.write(json.dumps(di))
		blogs = db.GqlQuery("select * from Blogs order by created desc")
		blogs=list(blogs)
		dump=[]
		for blog in blogs:
			d = {"subject": blog.subject ,"content": blog.content}
			dump.append(d)
		self.write(json.dumps(dump))


class LinkJson(Handler):
	def get(self,key):
		self.response.headers["Content-Type"] = "application/json"
		# di = {"a":[1], "b":key}
		# self.write(json.dumps(di))
		if key.isdigit():

			blog = Blogs.get_by_id(int(key))
			if blog:
				d = {"subject": blog.subject ,"content": blog.content}
				self.write(json.dumps(d))
			else:
				self.write("invalid request")
		else:
			self.write("totally invalid request")

class MainHandler(Handler): 
    def render_front(self, title="",art="",error=""):
    	blogs = db.GqlQuery("select * from Blogs order by created desc")
    	self.render("blogs.html", blogs = blogs)

    def get(self):
        self.render_front()

    
app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/newpost', AddpostHandler), ('/signup', SignupHandler), ('/welcome', WelcomeHandler), 
    ('/login',LoginHandler), ('/logout',LogoutHandler),
    ("/.json", Json), ("/(.+).json", LinkJson),
    ('(.+)',PermalinkHandler )
], debug=True)

#, ('(.+)',PermalinkHandler )

# key = self.request.route_args
# 		blog = Blogs.get_by_id(key[1])
# 		self.render("perma.html",blog=blog)