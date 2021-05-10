from django.urls import path, include
from . import views

app_name = 'automata'
urlpatterns = [
    path('files/', include('automata.file-urls')),
    path('editor/<int:pk>', views.EditUploadedFileFormView.as_view(), name="editor")
]
