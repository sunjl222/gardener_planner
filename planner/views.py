import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# 高德API的Key
AMAP_API_KEY = '865b15b3636b250390112ab3e5536084'

# 地理编码（地址转经纬度）
def geocode(address):
    url = f'https://restapi.amap.com/v3/geocode/geo?address={address}&key={AMAP_API_KEY}'
    response = requests.get(url)
    result = response.json()
    
    if result['status'] == '1' and result['geocodes']:
        lat_lng = result['geocodes'][0]['location'].split(',')
        return float(lat_lng[1]), float(lat_lng[0])  # 返回纬度和经度
    else:
        return None

# 路径规划（计算最优路径）
def optimize_route_planning(start, destinations):
    # 起点
    start_lat, start_lng = start['lat'], start['lng']
    
    # 转换目的地地址为经纬度
    destination_coords = []
    for dest in destinations:
        coords = geocode(dest)
        if coords:
            destination_coords.append(coords)
        else:
            return None  # 如果有地址无法解析，返回错误

    # 将目的地坐标传入高德路径规划接口
    waypoints = "|".join([f"{lng},{lat}" for lat, lng in destination_coords])  # 经纬度坐标串联
    url = f'https://restapi.amap.com/v3/direction/driving?origin={start_lng},{start_lat}&destination={destination_coords[-1][1]},{destination_coords[-1][0]}&waypoints={waypoints}&key={AMAP_API_KEY}'
    
    response = requests.get(url)
    result = response.json()
    
    if result['status'] == '1' and result['route']:
        route = result['route']['paths'][0]['steps']  # 获取最优路径步骤
        return [step['instruction'] for step in route]  # 返回路线的指示
    else:
        return None

@csrf_exempt
def optimize_route(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            start = data.get("start")
            destinations = data.get("destinations", [])
            
            if not start or not destinations:
                return JsonResponse({"error": "缺少起点或目的地"}, status=400)
            
            # 获取最优路线
            route_instructions = optimize_route_planning(start, destinations)
            if route_instructions is None:
                return JsonResponse({"error": "路线规划失败，请检查地址"}, status=400)

            return JsonResponse({"route": route_instructions})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "只支持POST请求"}, status=405)
