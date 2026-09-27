
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from agent import agent_go, ResearchResponse

app = FastAPI(
    title="ContextWeb-AI API",
    description="API RESTful para el Agente Autónomo de Investigación ContextWeb-AI",
    version="1.0.0"
)

# CORS CONEXION

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ResearchRequest(BaseModel):
    query: str = Field(..., example="¿Cuáles son las últimas novedades de LangChain?", description="Consulta de investigación para el agente")

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "online",
        "service": "ContextWeb-AI API",
        "version": "1.0.0"
    }

@app.post("/api/v1/research", response_model=ResearchResponse)
async def research_endpoint(request: ResearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="La consulta no puede estar vacía")
    
    try:
        result = await agent_go.run(request.query)
        return result
    except Exception as e:
        print(f"\n ERROR EN EL AGENTE: {e}\n") 
        raise HTTPException(status_code=500, detail=str(e))