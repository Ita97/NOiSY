
from django.urls import path
from . import views

app_name = 'Noise_Pollution'
urlpatterns = [
    path('', views.index, name='index'),
    path('sensor_list/', views.sensors, name='sensors'),
    path('<int:id>/', views.chart, name='chart'),
    path('send_data/<int:id>/', views.send_data, name='send_data'),
    path('add_sensor/', views.add_sensor, name='add_sensor'),
    path('room_list/', views.rooms, name='rooms'),
    path('manage_sensors/', views.manage_sensors, name='manage_sensors'),
    path('room/<int:id>/', views.room_sensors, name='room_sensors'),
    path('change_time_collection/<int:id>/', views.change_time_collection, name="change_time_collection"),
    path('move_sensor/<int:id>/', views.move_sensor, name='move_sensor'),
    path('delete_sensor/<int:id>/', views.delete_sensor, name='delete_sensor'),
    path('delete_room/<int:id>/', views.delete_room, name='delete_room'),
    path('add_room/', views.add_room, name='add_room'),
    path('<int:id>/chart_data/', views.ChartData.as_view(), name='chart_data'),
    path('<int:id>/history_one_day/<str:data>', views.history_chart, name='history_one_day'),
    path('<int:id>/history_more_days/<str:datastart>/<str:dataend>', views.history_chart2, name='history_one_day2')
    ]
