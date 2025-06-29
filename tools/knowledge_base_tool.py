# tools/knowledge_base_tool.py

import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class KnowledgeSearchInput(BaseModel):
    query: str = Field(description="需要在本地知识库中搜索的相关问题")

@tool(args_schema=KnowledgeSearchInput)
def search_knowledge_base(query: str) -> str:
    """
    当用户的问题可能与“旅游注意事项”、“行前准备”或“交通指南”等本地文档内容相关时，使用此工具在知识库中进行搜索。
    """
    # 确保 OPENAI_API_KEY 环境变量已设置
    if not os.getenv("OPENAI_API_KEY"):
        return "错误：管理员未配置 OpenAI API Key。"

    doc_path = os.path.join("docs", "旅游注意事项.pdf")

    if not os.path.exists(doc_path):
        return "错误：知识库文档 '旅游注意事项.pdf' 未找到。"

    try:
        loader = PyPDFLoader(doc_path)
        documents = loader.load()
        
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(docs, embeddings)
        
        # 检索最相关的3个文档块
        retrieved_docs = db.similarity_search(query, k=3)
        
        if not retrieved_docs:
            return "在知识库中没有找到相关信息。"
            
        # 将检索到的内容格式化为字符串返回
        content = "\n\n".join([doc.page_content for doc in retrieved_docs])
        return f"从知识库中找到以下相关信息：\n---\n{content}\n---"

    except Exception as e:
        return f"查询知识库时发生错误: {e}"

if __name__ == '__main__':
    # 本地测试
    os.environ["OPENAI_API_KEY"] = "sk-..." # 在这里填入你的key进行测试
    print(search_knowledge_base.invoke({"query": "去北京旅游，交通方面有什么建议？"}))
    print(search_knowledge_base.invoke({"query": "订酒店有什么要注意的？"}))