# main.py (示例)

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 导入你刚刚创建的工具
from tools.weather_tool import get_weather

# 2. 将所有工具放入一个列表
#    未来，知识库工具和本地函数工具也会被加到这里
tools = [get_weather]

# 3. 初始化大语言模型 (LLM)
#    确保 OPENAI_API_KEY 环境变量已设置
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# 4. 创建 Prompt 模板
#    这个模板至关重要，它告诉 Agent 如何行动，并为“记忆模块”预留了位置
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个乐于助人的旅游助手。"),
    # `chat_history` 占位符，用于实现记忆功能
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    # `agent_scratchpad` 占位符，是 Agent 思考过程的“草稿纸”
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 5. 创建 Agent
agent = create_openai_tools_agent(llm, tools, prompt)

# 6. 创建 Agent 执行器 (Executor)
#    `verbose=True` 可以打印出 Agent 的完整思考链，非常便于调试
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 7. 运行 Agent 并进行对话
if __name__ == '__main__':
    # 第一次对话
    response = agent_executor.invoke({
        "input": "你好，我想去北京旅游，能帮我查下今天那里的天气吗？"
    })
    print("AI:", response["output"])
    
    # 第二次对话（由于我们还没实现记忆模块，这里只是演示形式）
    # response = agent_executor.invoke({
    #     "input": "听起来不错，那上海呢？",
    #     "chat_history": [ ... 上一轮的对话历史 ... ]
    # })
    # print("AI:", response["output"])