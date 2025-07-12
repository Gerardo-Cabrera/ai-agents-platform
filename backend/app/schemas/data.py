from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AnalysisType(str, Enum):
    """Tipos de análisis de datos."""
    EXPLORATORY = "exploratory"
    STATISTICAL = "statistical"
    VISUALIZATION = "visualization"
    PREDICTION = "prediction"
    CLUSTERING = "clustering"
    CLASSIFICATION = "classification"

class DataSource(BaseModel):
    """Esquema para fuente de datos."""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., description="Tipo de fuente (csv, json, api, etc.)")
    url: Optional[str] = None
    file_path: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DataAnalysisRequest(BaseModel):
    """Esquema para solicitud de análisis de datos."""
    query: str = Field(..., min_length=1, max_length=2000)
    data_source_id: Optional[str] = None
    analysis_type: AnalysisType = AnalysisType.EXPLORATORY
    parameters: Optional[Dict[str, Any]] = None
    user_id: Optional[int] = None

class DataAnalysisResponse(BaseModel):
    """Esquema para respuesta de análisis de datos."""
    id: str
    query: str
    result: str
    analysis_type: AnalysisType
    data_source_id: Optional[str] = None
    processing_time: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None
    visualizations: Optional[List[str]] = None

class DataUploadRequest(BaseModel):
    """Esquema para solicitud de carga de datos."""
    filename: str = Field(..., min_length=1, max_length=255)
    file_type: str = Field(..., description="Tipo de archivo (csv, json, xlsx, etc.)")
    description: Optional[str] = None

class DataUploadResponse(BaseModel):
    """Esquema para respuesta de carga de datos."""
    id: str
    filename: str
    file_path: str
    file_size: int
    rows: Optional[int] = None
    columns: Optional[List[str]] = None
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    status: str = "uploaded"

class DataPreview(BaseModel):
    """Esquema para vista previa de datos."""
    data_source_id: str
    preview_data: List[Dict[str, Any]]
    total_rows: int
    total_columns: int
    column_types: Dict[str, str]
    sample_size: int = 10

class AnalysisResult(BaseModel):
    """Esquema para resultado de análisis."""
    analysis_id: str
    title: str
    description: str
    result_type: str
    data: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = None

class DataSourceList(BaseModel):
    """Esquema para lista de fuentes de datos."""
    data_sources: List[DataSource]
    total: int
    page: int
    per_page: int

class AnalysisHistory(BaseModel):
    """Esquema para historial de análisis."""
    analyses: List[DataAnalysisResponse]
    total: int
    page: int
    per_page: int

class WebSocketDataMessage(BaseModel):
    """Esquema para mensajes WebSocket de datos."""
    type: str = Field(..., description="Tipo de mensaje")
    data: Dict[str, Any] = Field(..., description="Datos del mensaje")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
