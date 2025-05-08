from django.apps import AppConfig
from django.conf import settings


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        # Avoid running twice in development
        if settings.DEBUG:
            import os
            if os.environ.get('RUN_MAIN', None) != 'true':
                return
                
        # Schedule periodic tasks
        from django_q2.tasks import schedule
        from django_q2.models import Schedule
        
        # Delete any existing schedules with the same name
        Schedule.objects.filter(name='update_movie_embeddings').delete()
        
        # Schedule the embedding updates to run daily
        schedule(
            'movie.tasks.update_movie_embeddings',
            name='update_movie_embeddings',
            schedule_type='D',  # Daily
            repeats=-1,         # Repeat forever
            max_per_run=20      # Directly pass the parameter, not as kwargs
        )
