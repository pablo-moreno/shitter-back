from django.urls import path, include


app_name = 'shitter'

urlpatterns = [
    path('', include('shitter.api.urls', namespace='shitter_api')),
]
