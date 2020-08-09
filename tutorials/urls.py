from django.conf.urls import url 
from tutorials import views 
from django.urls import path, include
 
urlpatterns = [ 
    url(r'^api/covids$', views.covid_list),
    # url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
    # url(r'^api/tutorials/published$', views.tutorial_list_published)
    url(r'^api/scraping$', views.scraping),
    url(r'^api/predict$', views.predict),
    url(r'^api/scrapeTweets$', views.scrapeTweets)
    
]
