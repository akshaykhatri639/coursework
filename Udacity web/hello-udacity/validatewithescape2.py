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
form='''<form method="post">
What is your birthday?
<br>
<label>Day
<input name="day" value="%(day)s">
</label>
<label>Month
<input name="month" value="%(month)s">
</label>
<label>Year
<input name="year" value="%(year)s">
</label>
<br>
<div style="color:red">%(error)s</div>
<br>
<input type="submit">
</form>
'''
import webapp2


def valid_year(year):
  if year.isdigit():
    year = int(year)
    if year>=1900 and year<=2020:
      return year

def valid_day(day):
  if day.isdigit():
    if int(day)>0 and int(day)<=31:
      return int(day)    


class MainHandler(webapp2.RequestHandler):
  def write_form(self,error='',day='',year='',month=''):
    self.response.out.write(form % {'error':error, 'day': day,'month':month, 'year':year})

  def get(self):
    self.write_form()

  def valid_month(self,month):
    months = ['January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December']
    for m in months:
      if m.lower() == month.lower():
        return m


  def post(self):
    user_m = self.request.get('month')
    user_d = self.request.get('day')
    user_y = self.request.get('year')

    m=self.valid_month(user_m)
    d=valid_day(user_d)
    y=valid_year(user_y)

    

    if not (y and d and m):
      self.write_form('There was a error',cgi.escape(user_d, quote=True),cgi.escape(user_y, quote=True), cgi.escape(user_m, quote=True))
    else:
      self.response.out.write('thanks')
        		
    	

app = webapp2.WSGIApplication([
    ('/', MainHandler)], debug=True)
