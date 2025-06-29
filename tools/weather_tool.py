# tools/weather_tool.py
import os
import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    city: str = Field(description="需要查询天气的城市名称，例如 '北京' 或 'San Francisco'")

@tool(args_schema=WeatherInput)
def get_weather(city: str) -> str:
    """当你需要查询一个具体城市的实时天气时，应使用此工具。它会返回该城市的温度和天气状况。"""
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return "错误：管理员未配置OpenWeatherMap API密钥。"

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric", "lang": "zh_cn"}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"城市 '{city}' 的当前天气是：{description}，温度为 {temperature}°C。"
    except requests.exceptions.HTTPError:
        return f"错误：无法找到名为 '{city}' 的城市。"
    except Exception as e:
        return f"查询天气时发生未知错误: {e}"

if __name__ == '__main__':
    # 设置环境变量进行测试
    os.environ["OPENWEATHERMAP_API_KEY"] = "你自己的OpenWeatherMap Key"
    print(get_weather.invoke({"city": "伦敦"}))