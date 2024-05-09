"""
Оригинальный код взят с PythonToday и немного доработан
Ссылка на видео: https://youtu.be/IZOq_sOtLz0?si=tajJXjtHiJiWxniq
"""
__all__ = ["get_info_by_ip"]
import requests
import folium


def get_info_by_ip(ip: str = '127.0.0.1') -> tuple[dict[str, str], folium.Map] | str:
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
    except requests.exceptions.ConnectionError:
        return '[!] Проверьте интернет соединение'
    data = {
        '[IP]': response.get('query'),
        '[Int prov]': response.get('isp'),
        '[Org]': response.get('org'),
        '[Country]': response.get('country'),
        '[Region Name]': response.get('regionName'),
        '[City]': response.get('city'),
        '[ZIP]': response.get('zip'),
        '[Lat]': response.get('lat'),
        '[Lon]': response.get('lon'),
    }

    area = folium.Map(location=[response.get('lat'), response.get('lon')])
    folium.Marker([response.get('lat'), response.get('lon')], popup=response.get("city")).add_to(area)

    return data, area
