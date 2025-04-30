import requests
import json
from itertools import permutations
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 高德地图 API Key
AMAP_API_KEY = '865b15b3636b250390112ab3e5536084'
ROUTE_MODE = 'walking'  # 使用步行模式

# 地址转经纬度
def geocode(address, city='深圳'):
    url = f'https://restapi.amap.com/v3/geocode/geo?address={address}&city={city}&key={AMAP_API_KEY}'
    response = requests.get(url)
    result = response.json()

    if result['status'] == '1' and result['geocodes']:
        location = result['geocodes'][0]['location']
        lng, lat = map(float, location.split(','))
        return lat, lng
    else:
        return None

@csrf_exempt
def optimize_route(request):
    if request.method != "POST":
        return JsonResponse({"error": "只支持POST请求"}, status=405)

    try:
        data = json.loads(request.body)
        start = data.get("start")
        destinations = data.get("destinations", [])

        if not start or not destinations:
            return JsonResponse({"error": "缺少起点或目的地"}, status=400)

        # 地址转坐标
        geocoded = []
        for address in destinations:
            coords = geocode(address)
            if coords:
                geocoded.append({
                    "address": address,
                    "lat": coords[0],
                    "lng": coords[1]
                })
            else:
                return JsonResponse({"error": f"地址无法解析: {address}"}, status=400)

        # 穷举所有路径顺序，寻找最短路径
        best_order = []
        min_total_distance = float('inf')

        for perm in permutations(geocoded):
            total_distance = 0
            current = start

            for point in perm:
                url = (
                    f"https://restapi.amap.com/v3/direction/{ROUTE_MODE}?"
                    f"origin={current['lng']},{current['lat']}&"
                    f"destination={point['lng']},{point['lat']}&"
                    f"key={AMAP_API_KEY}"
                )
                resp = requests.get(url).json()
                if resp['status'] != '1' or not resp['route']['paths']:
                    break
                distance = int(resp['route']['paths'][0]['distance'])
                total_distance += distance
                current = {"lat": point['lat'], "lng": point['lng']}
            else:
                if total_distance < min_total_distance:
                    min_total_distance = total_distance
                    best_order = list(perm)

        if not best_order:
            return JsonResponse({"error": "路径规划失败"}, status=400)

        # 返回每段路径细节
        steps = []
        current = start

        for point in best_order:
            url = (
                f"https://restapi.amap.com/v3/direction/{ROUTE_MODE}?"
                f"origin={current['lng']},{current['lat']}&"
                f"destination={point['lng']},{point['lat']}&"
                f"key={AMAP_API_KEY}"
            )
            result = requests.get(url).json()

            if result['status'] == '1' and result['route']['paths']:
                path_data = result['route']['paths'][0]['steps']
                instructions = [step['instruction'] for step in path_data]

                coords = []
                for step in path_data:
                    if 'polyline' in step:
                        for point_str in step['polyline'].split(';'):
                            lng, lat = map(float, point_str.split(','))
                            coords.append([lng, lat])

                steps.append({
                    "destination": point['address'],
                    "instructions": instructions,
                    "path": coords
                })

                current = {"lat": point['lat'], "lng": point['lng']}
            else:
                return JsonResponse({"error": f"路径规划失败: {point['address']}"}, status=400)

        return JsonResponse({
            "routes": steps,
            "order": [point['address'] for point in best_order],
            "total_distance": min_total_distance
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
