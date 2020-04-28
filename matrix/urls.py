from django.urls import path
from . import views

app_name = 'matrix'

urlpatterns = {
            path('', views.welcome_page, name='welcome'),
            path('results/', views.results, name='results'),
            path('about/', views.about, name='about'),
}
