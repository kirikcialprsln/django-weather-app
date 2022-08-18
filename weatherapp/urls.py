from weatherapp import views
from weatherapp.views import weather_link
from django.urls import path

urlpatterns = [
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),

    path('', views.home, name="home"),
    path('edit-location/', views.location, name='edit-location'),
    path('information/', views.information, name='information'),
    path('weather/', views.weather, name='weather'),
    path('list-user/', views.list_user, name='list-user'),
    path('weather-api', weather_link, name='weather_api'),
    path('add', views.add, name='add'),
    path('edit-user/<int:id>', views.edit_user, name='update-user'),
    path('delete/<int:id>', views.delete_user, name='delete')

]
