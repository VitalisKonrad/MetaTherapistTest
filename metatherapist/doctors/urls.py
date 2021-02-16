#Add URL maps to redirect the base URL to our application
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # path('', RedirectView.as_view(url='catalog/', permanent=True), views.home, name='home')
    # path('', RedirectView.as_view(url='catalog/', permanent=True)),
    path('', views.doctor),
]
