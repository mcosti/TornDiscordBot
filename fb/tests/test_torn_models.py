from fb.torn import models
from fb.dummy import dummyTornRequest
from pprint import pprint
torn_data = models.TornData.from_data(data=dummyTornRequest)
pprint(torn_data.to_dict())

for event in torn_data.events:
    pprint(event)

for message in torn_data.messages:
    pprint(message)