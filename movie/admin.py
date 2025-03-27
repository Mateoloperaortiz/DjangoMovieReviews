from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'year', 'has_embedding', 'embedding_age')
    list_filter = ('genre', 'year', 'embedding_updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('embedding_updated_at', 'embedding_display')
    
    def has_embedding(self, obj):
        return obj.embedding is not None
    has_embedding.boolean = True
    has_embedding.short_description = 'Has Embedding'
    
    def embedding_age(self, obj):
        if not obj.embedding_updated_at:
            return 'Never'
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()
        age = now - obj.embedding_updated_at
        if age < timedelta(minutes=60):
            return f'{age.seconds // 60} minutes'
        elif age < timedelta(days=1):
            return f'{age.seconds // 3600} hours'
        else:
            return f'{age.days} days'
    embedding_age.short_description = 'Embedding Age'
    
    def embedding_display(self, obj):
        if not obj.embedding:
            return 'No embedding stored'
        return f'Vector with {len(obj.embedding)} dimensions'
    embedding_display.short_description = 'Embedding'