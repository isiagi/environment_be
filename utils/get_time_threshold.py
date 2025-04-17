from datetime import datetime, timedelta
from django.utils import timezone

def get_time_threshold(task_type):
    now = timezone.now()
    if task_type == 'daily':
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif task_type == 'weekly':
        start_of_week = now.date() - timedelta(days=now.weekday())
        return timezone.make_aware(datetime.combine(start_of_week, datetime.min.time()))
    return None
