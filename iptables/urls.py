from django.urls import path, include
from . import views


urlpatterns = [
    path('home/', views.index, name="home"),
    path('', views.index),
    path('delete/<str:chain>/<int:rule_id>',
         views.delete_rule_using_no),
    path('interface/<str:interface>/<str:chain>',
         views.interfaces_chain_view, name='interfaces')
]
