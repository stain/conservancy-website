from django.conf.urls import url, include
from conservancy.apps.contractpatch import views as cpatch_views

urlpatterns = [
    url(r'', cpatch_views.index),
]
