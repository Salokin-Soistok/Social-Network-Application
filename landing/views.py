from django.shortcuts import render  # Import the render function to render templates
from django.views import View  # Import the View class to create class-based views

class Index(View):  # Define a class-based view for the index page
    def get(self, request, *args, **kwargs):  # Handle GET requests
        return render(request, 'landing/index.html')  # Render the 'landing/index.html' template
