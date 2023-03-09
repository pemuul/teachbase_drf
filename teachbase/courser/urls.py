from django.urls import include, path

from .views import Courses, Course_id, Login, Logout, Register


urlpatterns = [
    path('', Courses, name="Courses"),
    path('<int:id>', Course_id, name="Course_id"),
    path('account/register/', Register, name="Register"),
    path('logout/', Logout, name='logout'),
    path('login/', Login, name='login'),
]