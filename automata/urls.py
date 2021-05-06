from django.urls import path, include
from . import views

app_name = 'automata'
urlpatterns = [
    path('files/', include('automata.file-urls')),
]
