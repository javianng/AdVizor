from django.db import models
from django.utils import timezone

# Create your models here.

class Advertisement(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    
    LOCATION_CHOICES = [
        ('Urban', 'Urban'),
        ('Rural', 'Rural'),
        ('Suburban', 'Suburban')
    ]
    
    AD_TYPE_CHOICES = [
        ('Banner', 'Banner'),
        ('Video', 'Video'),
        ('Text', 'Text'),
        ('Native', 'Native')
    ]
    
    AD_PLACEMENT_CHOICES = [
        ('Social Media', 'Social Media'),
        ('Search Engine', 'Search Engine'),
        ('Website', 'Website')
    ]
    
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    income = models.FloatField()
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    ad_type = models.CharField(max_length=10, choices=AD_TYPE_CHOICES)
    ad_topic = models.CharField(max_length=50)
    ad_placement = models.CharField(max_length=20, choices=AD_PLACEMENT_CHOICES)
    clicks = models.IntegerField()
    click_time = models.DateTimeField(default=timezone.now)
    conversion_rate = models.FloatField()
    ctr = models.FloatField()
    impressions = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Ensure click_time is timezone-aware
        if self.click_time and timezone.is_naive(self.click_time):
            self.click_time = timezone.make_aware(self.click_time)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ad_type} - {self.ad_topic} ({self.click_time.date()})"
