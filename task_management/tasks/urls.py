from tasks import views
from django.urls import path

app_name = 'tasks'

urlpatterns = [
    path('list/', views.ListTasksView.as_view(), name='list'),
    path('create/', views.CreateTaskView.as_view(), name='create'),
    path('<str:pk>/', views.TaskDetailsView.as_view(), name='details'),
    path('delete/<str:pk>/', views.DeleteTaskView.as_view(), name='delete'),
    path('update/<str:pk>/', views.UpdateTaskView.as_view(), name='update'),

]
