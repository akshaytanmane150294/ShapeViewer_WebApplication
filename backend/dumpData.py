import csv
import os
import django
from backend import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # apne project ke hisaab se change karein
django.setup()

from prisms.models import Prism

def import_data_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        objs = []
        for row in reader:
            height_value = float(row['height']) if row['height'] else None
            radius_value = float(row['radius']) if row['radius'] else None
            length_value = float(row['length']) if row['length'] else None
            width_value = float(row['width'].strip()) if row['width'].strip() else None

            obj = Prism(
                designation=row['designation'],
                length=length_value,
                width=width_value,
                height=height_value,
                radius=radius_value,
                prism_name=row['prism_name']
            )
            objs.append(obj)
        Prism.objects.bulk_create(objs)
        print(f"{len(objs)} records inserted successfully!")

if __name__ == '__main__':
    import_data_from_csv('data.csv')
