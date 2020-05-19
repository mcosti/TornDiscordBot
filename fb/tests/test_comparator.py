from fb.models import DataComparator
from fb.torn.models import TornData
from fb.dummy import dummyTornRequest, dummyTornRequest2


old_data = TornData.from_data(dummyTornRequest)
new_data = TornData.from_data(dummyTornRequest2)

comparator = DataComparator(old_data, new_data)
alerts = comparator.compute_alerts()

for alert in alerts:
    print(alert)