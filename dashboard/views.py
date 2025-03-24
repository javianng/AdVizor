from django.shortcuts import render
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncDate
from .models import Advertisement
import json
from datetime import datetime, timedelta
from django.db.models import Q

def get_date_range_count(days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=int(days))
    return Advertisement.objects.filter(click_time__range=[start_date, end_date]).count()

def dashboard(request):
    # Get filter parameters
    date_range = request.GET.get('date_range', '30')  # Default to last 30 days
    custom_start = request.GET.get('custom_start', '')
    custom_end = request.GET.get('custom_end', '')
    ad_type = request.GET.get('ad_type', '')
    location = request.GET.get('location', '')
    ad_topic = request.GET.get('ad_topic', '')
    
    # Base queryset
    queryset = Advertisement.objects.all()
    
    # Apply date filter
    if date_range == 'custom' and custom_start and custom_end:
        try:
            start_date = datetime.strptime(custom_start, '%Y-%m-%d')
            end_date = datetime.strptime(custom_end, '%Y-%m-%d')
            queryset = queryset.filter(click_time__range=[start_date, end_date])
        except ValueError:
            # If date parsing fails, default to last 30 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            queryset = queryset.filter(click_time__range=[start_date, end_date])
    elif date_range:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=int(date_range))
        queryset = queryset.filter(click_time__range=[start_date, end_date])
    
    # Apply other filters
    if ad_type:
        queryset = queryset.filter(ad_type=ad_type)
    if location:
        queryset = queryset.filter(location=location)
    if ad_topic:
        queryset = queryset.filter(ad_topic=ad_topic)
    
    # Calculate record counts for each time range
    time_range_counts = {
        '7': get_date_range_count(7),
        '30': get_date_range_count(30),
        '90': get_date_range_count(90),
        '180': get_date_range_count(180),
        '365': get_date_range_count(365),
    }
    
    # Get unique values for filters
    ad_types = list(Advertisement.objects.values_list('ad_type', flat=True).distinct())
    locations = list(Advertisement.objects.values_list('location', flat=True).distinct())
    ad_topics = list(Advertisement.objects.values_list('ad_topic', flat=True).distinct())
    
    # Calculate metrics
    total_clicks = queryset.aggregate(total_clicks=Sum('clicks'))['total_clicks'] or 0
    total_impressions = queryset.aggregate(total_impressions=Sum('impressions'))['total_impressions'] or 0
    avg_ctr = queryset.aggregate(avg_ctr=Avg('ctr'))['avg_ctr'] or 0
    avg_conversion = queryset.aggregate(avg_conversion=Avg('conversion_rate'))['avg_conversion'] or 0
    
    # Performance by ad type
    ad_type_performance = list(queryset.values('ad_type')
        .annotate(
            avg_ctr=Avg('ctr'),
            avg_conversion=Avg('conversion_rate'),
            total_clicks=Sum('clicks'),
            total_impressions=Sum('impressions')
        ))
    
    # Performance by location
    location_performance = list(queryset.values('location')
        .annotate(
            avg_ctr=Avg('ctr'),
            avg_conversion=Avg('conversion_rate'),
            total_clicks=Sum('clicks'),
            total_impressions=Sum('impressions')
        ))
    
    # Daily trends
    daily_trends = list(queryset.annotate(date=TruncDate('click_time'))
        .values('date')
        .annotate(
            total_clicks=Sum('clicks'),
            total_impressions=Sum('impressions'),
            avg_ctr=Avg('ctr')
        )
        .order_by('date'))
    
    # Ad topic performance
    topic_performance = list(queryset.values('ad_topic')
        .annotate(
            avg_ctr=Avg('ctr'),
            avg_conversion=Avg('conversion_rate'),
            total_clicks=Sum('clicks'),
            total_impressions=Sum('impressions')
        ))
    
    context = {
        'total_clicks': total_clicks,
        'total_impressions': total_impressions,
        'avg_ctr': round(avg_ctr * 100, 2) if avg_ctr else 0,
        'avg_conversion': round(avg_conversion * 100, 2) if avg_conversion else 0,
        'ad_type_performance': json.dumps(ad_type_performance),
        'location_performance': json.dumps(location_performance),
        'daily_trends': json.dumps(daily_trends, default=str),
        'topic_performance': json.dumps(topic_performance),
        # Filter data
        'ad_types': ad_types,
        'locations': locations,
        'ad_topics': ad_topics,
        'selected_date_range': date_range,
        'selected_ad_type': ad_type,
        'selected_location': location,
        'selected_ad_topic': ad_topic,
        'custom_start': custom_start,
        'custom_end': custom_end,
        'time_range_counts': time_range_counts,
    }
    
    return render(request, 'dashboard/dashboard.html', context)
