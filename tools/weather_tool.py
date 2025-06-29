import os
import requests # 这个库需要安装: pip install requests

def get_weather(city: str) -> str:
    """
    获取指定城市的实时天气信息。

    Args:
        city (str): 需要查询的城市名称, 例如 "北京"。

    Returns:
        str: 格式化后的天气信息字符串，如果出错则返回错误信息。
    """
    # 1. 从环境变量中安全地获取 API Key
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return "错误：未配置OpenWeatherMap API密钥。请检查环境变量。"

    # 2. 构建 API 请求 URL
    #    - units=metric 表示使用摄氏度
    #    - lang=zh_cn 表示使用中文描述
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "zh_cn"
    }

    try:
        # 3. 发送 HTTP GET 请求
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # 如果请求失败 (例如 404, 500), 会抛出异常

        # 4. 解析返回的 JSON 数据
        weather_data = response.json()

        # 5. 提取需要的信息并格式化输出
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        
        return f"{city}当前天气：{description}，温度：{temperature}°C。"

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return f"错误：找不到城市 '{city}'。请检查城市名称是否正确。"
        else:
            return f"HTTP 错误：{http_err}"
    except Exception as e:
        return f"查询天气时发生未知错误: {e}"

# --- 本地测试代码 ---
# 这部分代码只在直接运行此文件时执行，用于快速测试工具是否正常工作
if __name__ == "__main__":
    # 在提交代码前，先自己测试一下
    test_city = "上海"
    weather_report = get_weather(test_city)
    print(weather_report)
    
    test_city_fail = "火星"
    weather_report_fail = get_weather(test_city_fail)
    print(weather_report_fail)