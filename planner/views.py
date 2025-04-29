import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# 高德API的Key
AMAP_API_KEY = '865b15b3636b250390112ab3e5536084'

# 地址转经纬度
def geocode(address):
    url = f'https://restapi.amap.com/v3/geocode/geo?address={address}&key={AMAP_API_KEY}'
    response = requests.get(url)
    result = response.json()
    
    if result['status'] == '1' and result['geocodes']:
        lat_lng = result['geocodes'][0]['location'].split(',')
        return float(lat_lng[1]), float(lat_lng[0])  # 返回纬度和经度
    else:
        return None

# 按段进行路径规划
@csrf_exempt
def optimize_route(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            start = data.get("start")
            destinations = data.get("destinations", [])

            if not start or not destinations:
                return JsonResponse({"error": "缺少起点或目的地"}, status=400)

            steps = []
            current = start

            for dest in destinations:
                dest_coords = geocode(dest)
                if not dest_coords:
                    return JsonResponse({"error": f"地址无法解析: {dest}"}, status=400)

                # 请求每段路径
                url = f'https://restapi.amap.com/v3/direction/driving?origin={current["lng"]},{current["lat"]}&destination={dest_coords[1]},{dest_coords[0]}&key={AMAP_API_KEY}'
                response = requests.get(url)
                result = response.json()

                if result['status'] == '1' and result['route']['paths']:
                    instructions = result['route']['paths'][0]['steps']
                    steps.append({
                        "destination": dest,
                        "instructions": [step['instruction'] for step in instructions]
                    })
                    current = {"lat": dest_coords[0], "lng": dest_coords[1]}  # 更新当前位置
                else:
                    return JsonResponse({"error": f"路径规划失败: {dest}"}, status=400)

            return JsonResponse({"routes": steps})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "只支持POST请求"}, status=405)
