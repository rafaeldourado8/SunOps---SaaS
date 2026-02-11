from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from celery.result import AsyncResult

class TaskStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, task_id):
        task = AsyncResult(task_id)
        return Response({
            'task_id': task_id,
            'status': task.state,
            'ready': task.ready(),
            'result': task.result if task.ready() and task.successful() else None
        })
