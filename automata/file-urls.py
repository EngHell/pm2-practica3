from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('upload/', views.UploadFileFormView.as_view(), name="upload"),
    path('delete/<int:pk>', views.delete, name="delete")
]
