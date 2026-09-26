from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
from tools import search_Duck, search_wiki, save_to_txt
load_dotenv()

class ResearchReponse(BaseModel):
    topic: str
    summary: str
    tools_used: list[str]


iAI = ChatOpenAI(model="gpt-4o-mini")
# iAI2 = ChatAnthropic(model="claude-3-5-sonnet-latest")


tools = [search_wiki, search_Duck, save_to_txt]
agent = create_agent(
    model=iAI, 
    tools=tools,
    system_prompt=(
        """
        Eres un asistente de investigación que ayuda a generar artículos científicos.
        Responde a la consulta del usuario y detalla las herramientas utilizadas.
        """
    ),
    response_format=ResearchReponse
)

query = input("¿En que puedo ayudarte hoy?")
raw_response = agent.invoke({
    "messages": [
        {"role": "user", "content": query}
    ]
})

final_result = raw_response.get("structured_response")

print(final_result)

try:
    structure_response = raw_response.get("structured_response")

    if structure_response is None:
        raise ValueError("El agente no devolvio una respuesta con estrcutura valida")
except Exception as e:
    print("Error response", e, "Raw Response", raw_response )