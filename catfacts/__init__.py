import yaml
import json
import twilio.twiml
from twilio.rest import TwilioRestClient
from shove import Shove
from flask import Flask, request, abort
from random import choice


class CatFactsREST(object):

    def __init__(self, config):
        self.config = config
        self.apikeys = [s.strip() for s in self.config['apikeys'].split(',')]
        dburi = self.config['dburi']
        self.db = Shove(dburi)
        self.app = Flask(__name__)
        self.api = TwilioRestClient(
                self.config['SID'],
                self.config['token'])
        if 'numbers' not in self.db:
            self.db['numbers'] = []
        if 'facts' not in self.db:
            print "No catfacts found, run catfacts load"
            exit()
        self.db.sync()

        self.routes = {
                "/api/numbers/<num>": (self.remove_number, {"methods": ['DELETE',]}),
                "/api/numbers": (self.add_number, {"methods": ['POST',]}),
                "/api/callback": (self.twilio_callback, {"methods": ['GET',]}),
                "/api/facts": (self.add_facts, {"methods": ['POST',]})}
        map(
            lambda route: self.app.route(route,
                **self.routes[route][1])(self.routes[route][0]),
            self.routes)

    def add_number(self):
        """
        POST: /api/numbers
        """
        print "Adding numbers"
        try:
            j = request.values['json']
            data = json.loads(j)
        except Exception as e:
            return json.dumps(dict(
                success=False,
                message="Invalid data recieved"))
        try:
            if data['apikey'] not in self.apikeys:
                raise Exception
        except:
            return json.dumps(dict(
                succes=False,
                message="Unauthorized"))
        try:
            number = data['number']
            if number not in self.db['numbers']:
                self.db['numbers'].append(number)
                self.db.sync()
                self.api.sms.messages.create(
                to=number,
                from_="2037947419",
                body="Congrats, you have been signed up for catfacts, \
                        the Premire cat information service, you will \
                        receive hourly cat information")
                return json.dumps(dict(
                    success=True,
                    message="Added {0} to catfacts".format(number)))
            else:
                return json.dumps(dict(
                    success=False,
                    message="{0} is already signed up for catfacts".format(
                            number)))

        except KeyError:
            return json.dumps(dict(
                success=False,
                message="Not Enough paramters"))

    def remove_number(self, num):
        """
        DELETE: /api/numbers/<number>
        """
        if num in self.db:
            self.db['numbers'].remove(num)
            self.db.sync()
            return json.dumps(dict(
                success=True,
                message="Removed {0} from catfacts".format(num)))
        else:
            return json.dumps(dict(
                success=False,
                message="{0} is not signed up for catfacts".format(num)))

    def twilio_callback(self):
        """
        POST: /api/callback
        """
        response = twilio.twiml.Response()
        response.sms(choice(self.db['facts']))
        return str(response)

    def add_facts(self):
        """
        POST: /api/facts
        """
        try:
            data = json.loads(request.values['json'])
        except:
            return json.dumps(dict(
                success=False,
                message="Invalid data recieved"))
        try:
            if data['apikey'] not in self.apikeys:
                raise Exception
        except:
            return json.dumps(dict(
                succes=False,
                message="Unauthorized"))

        try:
            self.db['facts'].extend(data['facts'])
            self.db.sync()
            return json.dumps(dict(
                success=True,
                message='Added more cat facts'))
        except KeyError:
            return json.dumps(dict(
                success=False,
                message="not enough parameters"))

    def start(self):
        self.app.run(
                debug=True,
                host=self.config['host'],
                port=self.config['port'])


def load_facts(config):
    import requests
    import re
    db = Shove(config['dburi'])
    db['facts'] = []
    url1 = 'http://www.cats.alpha.pl/facts.htm'
    raw = requests.get(url1).text
    filtered = filter(
            lambda l: l.startswith('<li>'),
            map(lambda l: l.strip(), raw.split('\n')))
    stripped = map(lambda l: re.sub('<[^<]+?>', '', l), filtered)
    db['facts'].extend(stripped)
    db.sync()


def main():
    from sys import argv
    config = yaml.load(file("/etc/catfacts.yml").read())
    if argv[1] == "rest":
        cf = CatFactsREST(config)
        cf.start()
    elif argv[1] == "load":
        load_facts(config)
    elif argv[1] == "cron":
        pass
