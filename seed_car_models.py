"""Seed Django CarMake and CarModel from IBM car_records.json or demo data."""
import json
from pathlib import Path
from djangoapp.models import CarMake, CarModel

file = Path.cwd() / 'database/data/car_records.json'
items = json.loads(file.read_text())['cars']
count=0
for item in items:
    make,_=CarMake.objects.get_or_create(name=item['make'])
    _,created=CarModel.objects.get_or_create(car_make=make,name=item['model'],year=int(item['year']),
                              defaults={'type':item.get('bodyType','Other') if item.get('bodyType','Other') in dict(CarModel.TYPES) else 'Other'})
    count+=int(created)
print(f'Added {count} car models; total {CarModel.objects.count()}')
