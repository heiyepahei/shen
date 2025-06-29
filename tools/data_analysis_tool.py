# tools/data_analysis_tool.py
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import numpy as np

class DataInput(BaseModel):
    numbers_str: str = Field(description="一个用逗号分隔的数字字符串，例如 '10, 25, 5, 42'")

@tool(args_schema=DataInput)
def analyze_data(numbers_str: str) -> str:
    """当用户提供了一串数字并要求进行排序、计算或数据分析时，使用此工具。"""
    try:
        # 将字符串转换为数字列表
        numbers = [float(num.strip()) for num in numbers_str.split(',')]
        if not numbers:
            return "错误：输入的数字列表为空。"

        # 使用 numpy 进行计算
        arr = np.array(numbers)
        count = len(arr)
        total_sum = np.sum(arr)
        average = np.mean(arr)
        minimum = np.min(arr)
        maximum = np.max(arr)
        sorted_list = sorted(numbers)

        return (
            f"数据分析结果如下：\n"
            f"- 数量: {count}\n"
            f"- 总和: {total_sum}\n"
            f"- 平均值: {average:.2f}\n"
            f"- 最小值: {minimum}\n"
            f"- 最大值: {maximum}\n"
            f"- 升序排序: {sorted_list}"
        )
    except (ValueError, TypeError):
        return "错误：输入格式不正确。请提供一个用逗号分隔的数字字符串。"
    except Exception as e:
        return f"数据分析时发生错误: {e}"

if __name__ == '__main__':
    # 本地测试
    print(analyze_data.invoke({"numbers_str": "15, 8, 23, 4, 42, 16"}))
    print(analyze_data.invoke({"numbers_str": "hello, world"}))