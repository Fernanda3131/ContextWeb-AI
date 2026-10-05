
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from agent import agent_go, ResearchResponse

app = FastAPI(
    title="ContextWeb-AI API",
    description="API RESTful para el Agente Autónomo de Investigación ContextWeb-AI",
    version="1.0.0"
)


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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La consulta no puede estar vacía."
        )
    
    try:
        result = await agent_go.run(request.query)
        return result

    except Exception as e:
        error_msg = str(e)
        print(f"\nERROR CAPTURADO EN EL AGENTE: {error_msg}\n") 

        if "DNSError" in error_msg or "DNS error" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Error de conexión al resolver el dominio de las herramientas de búsqueda (Wikipedia/DuckDuckGo). Revisa tu conexión a internet o la configuración de herramientas."
            )

        if "10054" in error_msg or "RequestError" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="El servicio externo de búsqueda rechazó o cerró la conexión temporalmente por límite de peticiones."
            )

        if "ValidationError" in error_msg or "OutputParserException" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El agente no pudo generar una respuesta con la estructura JSON requerida. Intenta replantear la pregunta."
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado durante la investigación: {error_msg}"
        )