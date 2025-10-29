from datetime import datetime
from datetime import timedelta

dt=datetime.today()-timedelta(days=1)
print(dt)
print(dt.replace(day=1) )
current_cycle_end_date = (dt.replace(day=1) + timedelta(days=32))
print(current_cycle_end_date)
