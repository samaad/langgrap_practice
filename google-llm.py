from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="models/gemini-flash-latest")
# response = llm.invoke("tell in 10 sentence above langchain/langgraph with google gemini")
response = llm.invoke("How far is moon from the earth ?")

# print(response.text)
print(response)

