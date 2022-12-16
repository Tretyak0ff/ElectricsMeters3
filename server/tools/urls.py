from django.urls import path

from .views import index, by_location, by_electricmeter, LocationCreateView, report, report2


urlpatterns = [
    path('add/', LocationCreateView.as_view(), name='add'),
    path('<int:location_id>/', by_location, name='location'),
    path('<int:location_id>/<int:electricmeter_id>/', by_electricmeter, name='electricmeter'),
    path('report/', report, name='report'),
    path('report2/', report2, name='report'),
    path('', index, name='index'),
]

