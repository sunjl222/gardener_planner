from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def optimize_route(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            start = data.get("start")
            destinations = data.get("destinations", [])
            
            if not start or not destinations:
                return JsonResponse({"error": "缺少起点或目的地"}, status=400)
            
            route = [start] + destinations + [start]
            return JsonResponse({"route": route})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "只支持POST请求"}, status=405)