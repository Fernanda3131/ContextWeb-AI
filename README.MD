# ContextWeb AI 🔍🌐

**ContextWeb AI** es un agente autónomo de inteligencia artificial expuesto a través de una **API RESTful de alto rendimiento con FastAPI**. A diferencia de los buscadores tradicionales, este agente comprende el contexto de consultas complejas, planifica y ejecuta búsquedas en la web, extrae información relevante de múltiples herramientas y genera reportes consolidados y estructurados en formato **JSON** validados con **Pydantic**.

Este proyecto fue desarrollado para demostrar la implementación práctica de arquitecturas de agentes autónomos, integración de herramientas (*tool calling*), salidas estructuradas y creación de APIs listas para entornos de producción.

---

## 🚀 Características Clave

* **API RESTful Asíncrona:** Exposición de endpoints asíncronos (`async/await`) construidos con **FastAPI** para consumo desde cualquier cliente o interfaz web (React, Angular, móvil).
* **Navegación Autónoma y Herramientas Multi-Fuente:** Integra herramientas como **DuckDuckGo Search**, **Wikipedia API** y persistencia en archivos mediante herramientas personalizadas (*custom tools*).
* **Salida JSON Estructurada:** Garantiza respuestas predecibles y estrictas utilizando validación de esquemas con **Pydantic** (`topic`, `summary`, `sources`, `tools_used`).
* **Soporte CORS y Documentación OpenAPI:** Configurado con políticas CORS globales y documentación interactiva autogenerada vía **Swagger UI**.

---

## 🛠️ Arquitectura y Tecnologías

El proyecto implementa una separación limpia entre la capa de red/servidor (FastAPI) y la lógica del agente autónomo (LangChain / LangGraph):

* **Backend & API Framework:** [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) (Servidor ASGI).
* **Core de IA & Orquestación:** [LangChain](https://www.langchain.com/) / [LangGraph](https://langchain-ai.github.io/langgraph/) con integración de modelos de OpenAI (`gpt-4o-mini`).
* **Herramientas de Búsqueda:** `duckduckgo-search`, `wikipedia` API wrapper y script de persistencia custom (`save_to_txt`).
* **Validación de Datos:** [Pydantic v2](https://docs.pydantic.dev/).

```mermaid
graph TD
    A[Cliente / Frontend] -->|POST /api/v1/research| B[FastAPI - main.py]
    B -->|Invocación Asíncrona| C[AgentGo - agent.py]
    C -->|Orquestación| D{Agente de IA - gpt-4o-mini}
    D -->|Tool Calling| E[DuckDuckGo Search]
    D -->|Tool Calling| F[Wikipedia API]
    D -->|Tool Calling| G[Save to File Tool]
    E --> D
    F --> D
    G --> D
    D -->|Parsing con Pydantic| H[ResearchResponse JSON]
    H --> B
    B -->|HTTP 200 OK| A