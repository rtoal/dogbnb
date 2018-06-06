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

class Reservation:
    def __init__(self, client_type, name, email, from_date, to_date):
        self.client_type = client_type
        self.name = name
        self.email = email
        self.from_date = from_date
        self.to_date = to_date

reservations = []

def find_dog_for_host(host):
    for reservation in reservations:
        if reservation.client_type == 'dog' and \
                reservation.from_date > host.from_date and \
                reservation.to_date < host.to_date:
            return reservation.email
    return None

def find_host_for_dog(dog):
    for reservation in reservations:
        if reservation.client_type == 'host' and \
                reservation.from_date < dog.from_date and \
                reservation.to_date > dog.to_date:
            return reservation.email
    return None

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
        reservation = Reservation(client_type, name, email, from_date, to_date)

        # NO ERROR CHECKING FOR NOW

        # put into database (optional)
        # food_record = Food(food_name = the_fav_food)
        # food_record.put()

        # TODO: CHECK FOR MATCH
        if client_type == 'host':
            email_to_contact = find_dog_for_host(reservation)
            if email_to_contact is None:
                reservations.append(reservation)
        elif client_type == 'dog':
            email_to_contact = find_host_for_dog(reservation)
            if email_to_contact is None:
                reservations.append(reservation)

        variable_dict = {'email_to_contact': email_to_contact}
        match_template = the_jinja_env.get_template("templates/match.html")
        self.response.write(match_template.render(variable_dict))

app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/match', MatchHandler)
], debug=True)
