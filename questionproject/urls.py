"""questionproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from polls import views
from polls.views import DetailView, ResultView, IndexView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url = 'polls/'), name = 'home'),
    path('polls/', IndexView.as_view(), name='index'),
    path('polls/<int:pk>/', DetailView.as_view(), name='detail'),
    path('polls/<int:question_id>/vote', views.vote, name ='vote'),
    path('polls/<int:pk>/result', ResultView.as_view(), name ='result'),
]
