from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import public, private

app = FastAPI(
    title="🌱 ECO_STREAM BIOTECH",
    description="### Sistema de Inteligencia Agrícola\nGestión avanzada de cultivos y suelos.",
    version="3.0.0",
    docs_url=None, 
    redoc_url=None
)

# CORS setup for possible frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public.router)
app.include_router(private.router)

# Redirigir la raíz para que al entrar se muestre la interfaz de la API y no un 404
@app.get("/", include_in_schema=False)
async def root():
    return HTMLResponse("""
    <!doctype html>
    <html>
      <head>
        <title>ECO_STREAM | Docs API</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style> 
          body { margin: 0; background-color: #f8fafc; font-family: sans-serif; } 
        </style>
      </head>
      <body>
        <script 
          id="api-reference" 
          data-url="/openapi.json"
          data-configuration='{
            "theme": "defaut",
            "forceDarkModeState": "light", 
            "showSidebar": true,
            "customCss": ":root { --scalar-color-accent: #10b981; --scalar-color-ghost: #ecfdf5; }"
          }'>
        </script>
        <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
      </body>
    </html>
    """)

@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return RedirectResponse(url="/")