import random

import yaml
from shove import Shove

from twilio.rest import TwilioRestClient

client = TwilioRestClient(account_sid, auth_token)
config = yaml.load(file(argv[1]).read())
db = Shove(config['dburi'])

for number in db['numbers']:

    while true:
        catfact = random.choice(db['facts'])
        if len(catfact) < 140:
            break

    message = client.sms.messages.create(to=number, from_=config['from_number'], body=catfact)
