import pandas as pd
from django.core.management.base import BaseCommand
from dashboard.models import Advertisement
from datetime import datetime

class Command(BaseCommand):
    help = 'Import advertisement data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        self.stdout.write(self.style.SUCCESS(f'Reading data from {csv_file_path}'))
        
        # Read the CSV file
        try:
            df = pd.read_csv(csv_file_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully read {len(df)} records'))
            
            # Clear existing data
            Advertisement.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing data'))
            
            # Import the data
            for _, row in df.iterrows():
                ad = Advertisement(
                    age=row['Age'],
                    gender=row['Gender'],
                    income=row['Income'],
                    location=row['Location'],
                    ad_type=row['Ad Type'],
                    ad_topic=row['Ad Topic'],
                    ad_placement=row['Ad Placement'],
                    clicks=row['Clicks'],
                    click_time=datetime.strptime(row['Click Time'], '%Y-%m-%d %H:%M:%S.%f') if isinstance(row['Click Time'], str) else row['Click Time'],
                    conversion_rate=row['Conversion Rate'],
                    ctr=row['CTR']
                )
                ad.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(df)} records'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}')) 