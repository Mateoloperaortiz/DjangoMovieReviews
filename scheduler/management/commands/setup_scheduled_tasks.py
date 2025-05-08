from django.core.management.base import BaseCommand
from django_q.tasks import schedule
from django_q.models import Schedule

class Command(BaseCommand):
    help = 'Creates or updates the scheduled tasks for the application.'

    def handle(self, *args, **options):
        self.stdout.write('Setting up scheduled tasks...')

        # Delete any existing schedules with the same name to ensure idempotency
        Schedule.objects.filter(name='update_movie_embeddings').delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted existing "update_movie_embeddings" schedule (if any).'))

        # Schedule the embedding updates to run daily
        schedule(
            'movie.tasks.update_movie_embeddings',
            name='update_movie_embeddings',
            schedule_type='D',  # Daily
            repeats=-1,         # Repeat forever
            max_per_run=20
        )
        self.stdout.write(self.style.SUCCESS('Successfully scheduled "update_movie_embeddings" task.'))
