from datetime import datetime, timedelta, timezone


now = (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")

# print(now.days)


print(now)