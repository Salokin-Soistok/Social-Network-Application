from django.urls import path  # Import the path function to define URL patterns
from landing.views import Index  # Import the Index view from the landing app's views

urlpatterns = [  # Define a list of URL patterns
    path('', Index.as_view(), name='index'),  # Map the root URL ('') to the Index view; name it 'index' for reverse lookups
]
