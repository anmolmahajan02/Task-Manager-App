from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name='index'),
    path("addTasks",views.addTasks,name='addTasks'),
    path("yourTasks",views.yourTasks,name='yourTasks'),
    path("login",views.login,name='login'),
    path("register",views.register,name='register'),
    path("logout",views.logout,name='logout'),
    path('allTasks',views.allTasks,name='allTasks'),
    path('delete<int:delId>/',views.delete,name = 'delete'),
    path('fullTask<int:fullId>/',views.fullTask,name = 'fullTask'),
]