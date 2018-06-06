# Copyright 2016 Google Inc.
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

import webapp2
import jinja2
import os

class Availability:
    def __init__(self, type, name, email, from_date, to_date):
        self.type = type
        self.name = name
        self.email = email
        self.from_date = from_date
        self.to_date = to_date

availaibities = []

def find_dog_for_host(host):
    pass

def find_host_for_dog(dog):
    pass

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        main_template = the_jinja_env.get_template('templates/index.html')
        self.response.write(main_template.render())

class MatchHandler(webapp2.RequestHandler):
    def get(self):
        client_type = self.request.get('client-type')
        name = self.request.get('name')
        email = self.request.get('email')
        from_date = self.request.get('client-from')
        to_date = self.request.get('client-to')

        # NO ERROR CHECKING FOR NOW

        # put into database (optional)
        # food_record = Food(food_name = the_fav_food)
        # food_record.put()

        # TODO: CHECK FOR MATCH

        email = 'ThisIsFake@example.com'

        variable_dict = {'email_to_contact': email}
        match_template = the_jinja_env.get_template("templates/match.html")
        self.response.write(match_template.render(variable_dict))

app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/match', MatchHandler)
], debug=True)
