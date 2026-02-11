from django.urls import path
from .views import DashboardResumoView
from .monitoring import TaskStatusView

urlpatterns = [
    path('resumo/', DashboardResumoView.as_view(), name='dashboard-resumo'),
    path('tasks/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
]
