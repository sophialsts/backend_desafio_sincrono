from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from routes import pesquisadores_router, producoes_router

app = FastAPI(
    title="API de Pesquisadores e Produções",
    description="API RESTful para gerenciamento de pesquisadores e suas produções científicas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pesquisadores_router)
app.include_router(producoes_router)


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API FastAPI - Pesquisadores</title>
        <style>
            body {
                font-family: system-ui, -apple-system, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            h1 { color: #333; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
            code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>API FastAPI - Pesquisadores e Produções</h1>
            <p>API RESTful com operações CRUD para gerenciamento de pesquisadores e produções científicas.</p>
            <p><a href="/docs">Acesse a documentação interativa (Swagger UI)</a></p>
            <p><a href="/redoc">Acesse a documentação (ReDoc)</a></p>
        </div>
        <div class="card">
            <h2>Endpoints disponíveis:</h2>
            <ul>
                <li><code>GET /pesquisadores</code> - Listar todos os pesquisadores</li>
                <li><code>GET /pesquisadores/{lattes_id}</code> - Buscar pesquisador</li>
                <li><code>DELETE /pesquisadores/{lattes_id}</code> - Deletar pesquisador</li>
            </ul>
            <ul>
                <li><code>POST /producoes</code> - Criar nova produção</li>
                <li><code>GET /producoes/{producoes_id}</code> - Buscar produção específica</li>
                <li><code>PUT /producoes/{producoes_id}</code> - Atualizar produção</li>
                <li><code>DELETE /producoes/{producoes_id}</code> - Deletar produção</li>
            </ul>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
