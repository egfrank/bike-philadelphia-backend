from api.models import Snapshot
from datetime import datetime, timedelta

base = datetime.now()
date_list = [base - timedelta(hours=x) for x in range(0, 240)]
date_list.reverse()


for i, timestamp in enumerate(date_list):
    Snapshot.objects.create(
        timestamp=timestamp,
        stations={
            3004: {'station': i},
            3005: {'station': i},
        },
        weather={
            'weather': i}
    )