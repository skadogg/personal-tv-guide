from django.db import models

# Create your models here.
class Title(models.Model):
    # Core identifying information
    title = models.CharField(max_length=255, db_index=True)
    object_type = models.CharField(max_length=10) # 'movie' or 'show'
    
    # JustWatch data
    justwatch_id = models.IntegerField(unique=True, null=True, blank=True, db_index=True)
    justwatch_url = models.URLField(max_length=500, null=True, blank=True)
    
    # TMDB data
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True, db_index=True)
    poster_url = models.URLField(max_length=500, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    genres = models.CharField(max_length=500, null=True, blank=True) 
    release_date = models.DateField(null=True, blank=True)
    
    # Time/Episode data
    runtime_minutes = models.IntegerField(null=True, blank=True) 
    number_of_seasons = models.IntegerField(default=0)
    number_of_episodes = models.IntegerField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Watchlist Title"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.object_type})"