from django.contrib import admin
from .models import Advertisement
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import DateTimeWidget, IntegerWidget, FloatWidget, CharWidget
from datetime import datetime
from django.core.files.storage import default_storage
from import_export.tmp_storages import MediaStorage

class AdvertisementResource(resources.ModelResource):
    # Define all fields explicitly with proper column mappings
    age = fields.Field(
        column_name='Age',
        attribute='age',
        widget=IntegerWidget()
    )
    gender = fields.Field(
        column_name='Gender',
        attribute='gender',
        widget=CharWidget()
    )
    income = fields.Field(
        column_name='Income',
        attribute='income',
        widget=FloatWidget()
    )
    location = fields.Field(
        column_name='Location',
        attribute='location',
        widget=CharWidget()
    )
    ad_type = fields.Field(
        column_name='Ad Type',
        attribute='ad_type',
        widget=CharWidget()
    )
    ad_topic = fields.Field(
        column_name='Ad Topic',
        attribute='ad_topic',
        widget=CharWidget()
    )
    ad_placement = fields.Field(
        column_name='Ad Placement',
        attribute='ad_placement',
        widget=CharWidget()
    )
    clicks = fields.Field(
        column_name='Clicks',
        attribute='clicks',
        widget=IntegerWidget()
    )
    click_time = fields.Field(
        column_name='Click Time',
        attribute='click_time',
        widget=DateTimeWidget(format='%Y-%m-%d %H:%M:%S.%f')
    )
    conversion_rate = fields.Field(
        column_name='Conversion Rate',
        attribute='conversion_rate',
        widget=FloatWidget()
    )
    ctr = fields.Field(
        column_name='CTR',
        attribute='ctr',
        widget=FloatWidget()
    )

    def before_import_row(self, row, **kwargs):
        """
        Clean and validate data before import
        """
        # Handle numeric fields
        try:
            # Age handling
            row['Age'] = max(0, int(float(row['Age']))) if row['Age'] else 0
            
            # Income handling
            row['Income'] = float(row['Income']) if row['Income'] else 0.0
            
            # Clicks handling
            row['Clicks'] = int(float(row['Clicks'])) if row['Clicks'] else 0
            
            # CTR and Conversion Rate handling
            row['CTR'] = float(row['CTR']) if row['CTR'] else 0.0
            row['Conversion Rate'] = float(row['Conversion Rate']) if row['Conversion Rate'] else 0.0
            
            # Calculate impressions
            ctr = float(row['CTR'])
            clicks = int(float(row['Clicks']))
            if ctr > 0:
                impressions = int(round(clicks / ctr))
            else:
                impressions = max(clicks, 1)  # At least as many impressions as clicks
            row['impressions'] = impressions
            
        except (ValueError, TypeError) as e:
            # Set default values if conversion fails
            row['Age'] = 0
            row['Income'] = 0.0
            row['Clicks'] = 0
            row['CTR'] = 0.0
            row['Conversion Rate'] = 0.0
            row['impressions'] = 0
        
        # Ensure string fields are properly formatted
        row['Gender'] = str(row.get('Gender', '')).strip()
        row['Location'] = str(row.get('Location', '')).strip()
        row['Ad Type'] = str(row.get('Ad Type', '')).strip()
        row['Ad Topic'] = str(row.get('Ad Topic', '')).strip()
        row['Ad Placement'] = str(row.get('Ad Placement', '')).strip()

    def get_instance(self, instance_loader, row):
        """
        Handle duplicate entries based on unique fields
        """
        return None  # Always create new instances

    class Meta:
        model = Advertisement
        import_id_fields = []
        fields = ('age', 'gender', 'income', 'location', 'ad_type', 'ad_topic', 
                 'ad_placement', 'clicks', 'click_time', 'conversion_rate', 
                 'ctr', 'impressions')
        exclude = ('id',)
        skip_unchanged = True
        report_skipped = True
        use_bulk = True
        batch_size = 1000

@admin.register(Advertisement)
class AdvertisementAdmin(ImportExportModelAdmin):
    resource_class = AdvertisementResource
    list_display = ('ad_type', 'ad_topic', 'location', 'clicks', 'impressions', 'ctr', 'conversion_rate', 'click_time')
    list_filter = ('ad_type', 'location', 'ad_topic', 'ad_placement')
    search_fields = ('ad_type', 'ad_topic', 'location', 'ad_placement')
    ordering = ('-click_time',)
    
    def get_import_formats(self):
        """
        Returns available import formats.
        """
        from import_export.formats import base_formats
        return [base_formats.CSV]
    
    class Media:
        js = ('admin/js/vendor/jquery/jquery.min.js',)  # Ensure jQuery is loaded
