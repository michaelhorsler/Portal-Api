import requests
import datetime
from dateutil import parser # type: ignore
from collections import deque
from datetime import datetime, timedelta, UTC

from dotenv import load_dotenv
import os

# === CONFIGURATION ===
token = os.environ.get("LOGGLY_QUERY_TOKEN")
LOGGLY_TAG = 'portalapi'
LOGGLY_QUERY = 'json.status:FAILURE OR json.status:RECOVERY'
TIME_RANGE_HOURS = 24  # Adjust as needed
print(token)
# === TIME RANGE ===
until_time = datetime.now(UTC)
from_time = until_time - timedelta(hours=24)

# === BUILD SEARCH API URL ===
search_url = (
    f'https://logs-01.loggly.com/apiv2/events/search'
    f'?q=tag:{LOGGLY_TAG}+AND+({LOGGLY_QUERY})'
    f'&from={from_time.isoformat()}Z&until={until_time.isoformat()}Z'
    f'&order=asc&size=1000'
)

headers = {
    'Authorization': f'Bearer {token}'
}

# === FETCH EVENTS ===
response = requests.get(search_url, headers=headers)
response.raise_for_status()

events = response.json().get('events', [])
failures = deque()
recoveries = deque()

for event in events:
    ts = parser.isoparse(event['event']['timestamp'])
    status = event['event'].get('json', {}).get('status')
    if status == 'FAILURE':
        failures.append(ts)
    elif status == 'RECOVERY':
        recoveries.append(ts)

# === CALCULATE METRICS ===
mttr_list = []
mttf_list = []

last_recovery_time = None

while failures:
    failure_time = failures.popleft()

    # Find the next recovery
    while recoveries and recoveries[0] <= failure_time:
        recoveries.popleft()

    if recoveries:
        recovery_time = recoveries.popleft()
        mttr = (recovery_time - failure_time).total_seconds()
        mttr_list.append(mttr)

        if last_recovery_time:
            mttf = (failure_time - last_recovery_time).total_seconds()
            mttf_list.append(mttf)

        last_recovery_time = recovery_time

# === OUTPUT ===
if mttr_list:
    avg_mttr = sum(mttr_list) / len(mttr_list)
    print(f"Average MTTR: {avg_mttr:.2f} seconds ({avg_mttr/60:.2f} minutes)")
else:
    print("No MTTR data available.")

if mttf_list:
    avg_mttf = sum(mttf_list) / len(mttf_list)
    print(f"Average MTTF: {avg_mttf:.2f} seconds ({avg_mttf/60:.2f} minutes)")
else:
    print("No MTTF data available.")
