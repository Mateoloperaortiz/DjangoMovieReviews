import time
from django.core.management.base import BaseCommand
from django_q.cluster import Cluster
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the Django Q cluster for task processing'

    def handle(self, *args, **options):
        self.stdout.write('Starting Django Q cluster for background tasks...')
        
        # Start the cluster
        cluster = Cluster()
        cluster.start()
        
        try:
            # Keep the cluster running
            while True:
                time.sleep(10)
                status = cluster.stat
                self.stdout.write(f"Workers: {status.workers} | "
                                 f"Queued: {status.queue} | "
                                 f"Processed: {status.processed}")
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Stopping cluster...'))
            cluster.stop()
            self.stdout.write(self.style.SUCCESS('Cluster stopped')) 