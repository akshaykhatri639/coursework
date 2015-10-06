


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
import cgi
form='''
<form method="post">
<br>
<label>Username<input type="text" name="username" value="%(name)s"> %(nameerror)s </label>
<br>
<label>Password
<input type="password" name="password" > %(passerror)s
</label> <br>
<label>Verify password
<input type="password" name="verify" > %(verifyerror)s
</label><br>
<label>email(optional)
<input type="text" name="text" value="%(mail)s"> %(mailerror)s
</label><br>

<input type="submit">
</form>
'''

import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
  return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_pass(password):
  return PASS_RE.match(password)

MAIL_RE=re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_mail(mail):
  return not mail or MAIL_RE.match(mail)


class MainHandler(webapp2.RequestHandler):
  def write_form(self, name="",mail="",nameerror="", mailerror="",verifyerror="", passerror=""):
    self.response.out.write(form % {"name":name, "mail":mail, "nameerror":nameerror, "mailerror":mailerror, "verifyerror":verifyerror, "passerror":passerror})

  def get(self):
    self.write_form()

  def post(self):
    n=False
    p=False
    v=False
    e=False
    nameerror=""
    mailerror="abc"
    verifyerror=""
    passerror=""
    username=self.request.get("username")
    password=self.request.get("password")
    verify=self.request.get("verify")
    email=self.request.get("email")
    n=valid_username(username)
    p=valid_username(password)
    e=valid_mail(email)
    if not n:
      nameerror="Please enter a valid username"

    if not p:
      passerror="Please enter a valid password"

    if password != verify:
      verifyerror="Passwords do not match"
    else:
      v=True    

    if not e:
      mailerror="Please enter a valid email"


    if (not n) or  (not p) or (not v) or (not e):
      self.write_form(username,email,nameerror, mailerror,verifyerror, passerror)
    else:
      self.redirect("/welcome?username=" + username)  


class WelcomeHandler(webapp2.RequestHandler):
  def get(self):
    name= self.request.get("username")
    self.response.out.write("Welcome, " + name)


app = webapp2.WSGIApplication([('/', MainHandler), ('/welcome',WelcomeHandler)], debug=True)
