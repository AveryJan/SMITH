#!/usr/bin/env python3
"""Import the genuine public IBM starter dataset; requires internet connection."""
from pathlib import Path
from urllib.request import urlopen
import json

root = Path(__file__).resolve().parents[1]
origin = 'https://raw.githubusercontent.com/ibm-developer-skills-network/xrwvm-fullstack_developer_capstone/main/server/database/data/'
destination = root / 'server' / 'database' / 'data'
destination.mkdir(parents=True, exist_ok=True)
for name, key in [('dealerships.json','dealerships'),('reviews.json','reviews'),('car_records.json','cars')]:
    with urlopen(origin+name, timeout=25) as response:
        payload = response.read()
    data = json.loads(payload)
    if not isinstance(data.get(key),list) or not data[key]:
        raise RuntimeError(f'Invalid IBM dataset for {name}')
    (destination/name).write_bytes(payload)
    print(f'Imported official {name}: {len(data[key])} records')
