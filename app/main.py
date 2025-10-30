import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import SessionLocal, engine
from app.db.models import Base
import logging
from contextlib import asynccontextmanager

# Criar tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for application lifespan events."""
    logger.info("🚀 Iniciando Recommendation ML API...")
    # Conectar ao Redis, etc.
    logger.info("✅ Aplicação iniciada com sucesso")
    yield
    logger.info("🛑 Encerrando aplicação...")

# Inicializar aplicação
app = FastAPI(
    title="Recommendation ML API",
    description="API de recomendações usando Machine Learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência do Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Incluir rotas
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "name": "Recommendation ML API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Tenta fazer uma consulta simples para verificar a conexão com o banco
        db.execute('SELECT 1')
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Erro no health check do banco de dados: {e}")
        db_status = "unhealthy"

    return {
        "status": "healthy",
        "db_status": db_status,
        "model_loaded": True, # Placeholder
        "cache_connected": True # Placeholder
    }