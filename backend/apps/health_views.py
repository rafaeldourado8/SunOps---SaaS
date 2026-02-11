from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from celery.result import AsyncResult
from django.core.cache import cache

class TaskStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, task_id):
        task = AsyncResult(task_id)
        
        response_data = {
            'task_id': task_id,
            'status': task.state,
            'ready': task.ready(),
        }
        
        if task.ready():
            if task.successful():
                response_data['result'] = task.result
            else:
                response_data['error'] = str(task.info)
        
        return Response(response_data)

class CacheStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from django_redis import get_redis_connection
        
        try:
            redis_conn = get_redis_connection("default")
            info = redis_conn.info()
            
            return Response({
                'connected_clients': info.get('connected_clients'),
                'used_memory_human': info.get('used_memory_human'),
                'total_commands_processed': info.get('total_commands_processed'),
                'keyspace_hits': info.get('keyspace_hits'),
                'keyspace_misses': info.get('keyspace_misses'),
                'hit_rate': round(
                    info.get('keyspace_hits', 0) / 
                    (info.get('keyspace_hits', 0) + info.get('keyspace_misses', 1)) * 100, 
                    2
                )
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class CeleryStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from config.celery import app
        
        try:
            inspect = app.control.inspect()
            
            return Response({
                'active_tasks': inspect.active(),
                'scheduled_tasks': inspect.scheduled(),
                'registered_tasks': list(app.tasks.keys()),
                'stats': inspect.stats(),
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)
