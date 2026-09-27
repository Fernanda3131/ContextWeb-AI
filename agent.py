import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.prebuilt import create_react_agent
from tools import search_Duck, search_wiki, save_to_txt

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str = Field(description="Tema principal investigado")
    summary: str = Field(description="Resumen detallado de la investigación")
    sources: list[str] = Field(description="Lista de fuentes consultadas")
    tools_used: list[str] = Field(description="Herramientas utilizadas por el agente")


class AgentGo:
    def __init__(self):
        self.iAI = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )
        self.tools = [search_wiki, search_Duck, save_to_txt]
        self.parser = PydanticOutputParser(pydantic_object=ResearchResponse)

        system_prompt = (
            "Eres un asistente de investigación web llamado ContextWeb-AI. "
            "Responde a la consulta del usuario utilizando las herramientas necesarias. "
            "Debes responder estrictamente en formato JSON siguiendo este esquema:\n"
            f"{self.parser.get_format_instructions()}"
        )

        self.agent_executor = create_react_agent(
            model=self.iAI,
            tools=self.tools,
            prompt=system_prompt
        )

    async def run(self, query: str) -> ResearchResponse:
        inputs = {"messages": [("user", query)]}
        response = await self.agent_executor.ainvoke(inputs)

        last_message = response["messages"][-1].content

        return self.parser.parse(last_message)


agent_go = AgentGo()