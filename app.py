# app.py

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 导入所有工具！张三和李四的工具都在这里集合
from tools.knowledge_base_tool import search_knowledge_base
from tools.weather_tool import get_weather
from tools.data_analysis_tool import analyze_data

# 1. 初始化模型和工具
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
tools = [search_knowledge_base, get_weather, analyze_data]

# 2. 创建 Agent Prompt
# 这是指导 Agent 如何思考的核心模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个全能的旅游助手。你能查询天气，从知识库回答问题，并进行简单的数据分析。请友好地回答用户问题。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 3. 创建 Agent
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. 设置记忆模块
# 我们使用一个简单的字典来存储每个用户的对话历史
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 5. 将记忆模块与 Agent 链接起来
# 这会创建一个新的、带有记忆功能的 Agent Executor
agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# 6. 启动一个交互式对话循环
if __name__ == "__main__":
    print("旅游助手已启动！输入 'exit' 退出。")
    session_id = "user123" # 为当前对话设置一个 session id

    while True:
        user_input = input("你: ")
        if user_input.lower() == 'exit':
            print("再见！")
            break
        
        response = agent_with_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        print("助手:", response["output"])