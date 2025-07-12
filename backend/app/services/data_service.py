import uuid
import time
import logging
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import os

# Optional Redis import for distributed caching
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

from app.schemas.data import (
    DataAnalysisRequest, DataAnalysisResponse, DataSource,
    AnalysisType, WebSocketDataMessage
)
from app.core.websocket_manager import manager

logger = logging.getLogger(__name__)

class DataService:
    """Service for data analysis with optional Redis caching for scalability."""
    
    def __init__(self):
        # Initialize Redis connection for distributed caching (optional)
        self.redis_available = False
        self.redis_client = None
        
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.Redis(
                    host=os.getenv('REDIS_HOST', 'localhost'),
                    port=int(os.getenv('REDIS_PORT', 6379)),
                    db=0,
                    decode_responses=True
                )
                # Test connection
                self.redis_client.ping()
                self.redis_available = True
                logger.info("Redis cache initialized successfully")
            except Exception as e:
                logger.warning(f"Redis not available, using in-memory cache: {e}")
                self.redis_available = False
                self.redis_client = None
        else:
            logger.info("Redis not installed, using in-memory cache")
        
        # Fallback to in-memory storage if Redis is not available
        self.data_sources: Dict[str, DataSource] = {}
        self.analyses: Dict[str, DataAnalysisResponse] = {}
        self.data_cache: Dict[str, pd.DataFrame] = {}
    
    def _get_cache_key(self, prefix: str, key: str) -> str:
        """Generate cache key with prefix."""
        return f"data_service:{prefix}:{key}"
    
    def _cache_set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache (Redis or memory)."""
        try:
            if self.redis_available and self.redis_client:
                if isinstance(value, pd.DataFrame):
                    # Convert DataFrame to JSON for Redis storage
                    value_json = value.to_json()
                    return self.redis_client.setex(key, expire, value_json)
                else:
                    return self.redis_client.setex(key, expire, json.dumps(value))
            else:
                # Fallback to in-memory cache
                self.data_cache[key] = value
                return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    def _cache_get(self, key: str) -> Any:
        """Get value from cache (Redis or memory)."""
        try:
            if self.redis_available and self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    # Try to parse as DataFrame first, then as JSON
                    try:
                        return pd.read_json(value)
                    except:
                        return json.loads(value)
            else:
                # Fallback to in-memory cache
                return self.data_cache.get(key)
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None
    
    async def process_data_analysis(self, request: DataAnalysisRequest) -> DataAnalysisResponse:
        """Processes a data analysis request."""
        start_time = time.time()
        
        try:
            analysis_id = str(uuid.uuid4())
            
            # Load data if a source is specified
            data = None
            if request.data_source_id and request.data_source_id in self.data_sources:
                data = await self._load_data(request.data_source_id)
            
            # Generate analysis
            result = await self._generate_analysis(request, data)
            
            processing_time = time.time() - start_time
            
            # Create response
            response = DataAnalysisResponse(
                id=analysis_id,
                query=request.query,
                result=result,
                analysis_type=request.analysis_type,
                data_source_id=request.data_source_id,
                processing_time=processing_time,
                timestamp=datetime.utcnow(),
                metadata={
                    "user_id": request.user_id,
                    "parameters": request.parameters
                }
            )
            
            # Save analysis
            self.analyses[analysis_id] = response
            
            # Send result via WebSocket
            await self._broadcast_analysis_result(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing data analysis: {e}")
            raise
    
    async def _generate_analysis(self, request: DataAnalysisRequest, data: Optional[pd.DataFrame]) -> str:
        """Generates analysis based on the query and data."""
        try:
            # Here you should integrate with the real LLM for data analysis
            # For now, we simulate basic analyses
            
            if data is not None:
                # Analysis with real data
                result = self._analyze_dataframe(data, request.query, request.analysis_type)
            else:
                # Analysis without data (general queries)
                result = self._generate_general_analysis(request.query, request.analysis_type)
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating analysis: {e}")
            return f"Error in analysis: {str(e)}"
    
    def _analyze_dataframe(self, df: pd.DataFrame, query: str, analysis_type: AnalysisType) -> str:
        """Performs analysis on a DataFrame."""
        try:
            result = f"Data Analysis:\n\n"
            result += f"Dataset: {len(df)} rows, {len(df.columns)} columns\n"
            result += f"Columns: {', '.join(df.columns.tolist())}\n\n"
            
            if analysis_type == AnalysisType.EXPLORATORY:
                result += "**Exploratory Analysis:**\n"
                result += f"- Data types:\n"
                for col in df.columns:
                    result += f"  - {col}: {df[col].dtype}\n"
                
                result += f"\n- Descriptive statistics:\n"
                result += df.describe().to_string()
                
            elif analysis_type == AnalysisType.STATISTICAL:
                result += "**Statistical Analysis:**\n"
                result += f"- Missing values:\n"
                result += df.isnull().sum().to_string()
                
                result += f"\n- Correlations:\n"
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 1:
                    result += df[numeric_cols].corr().to_string()
                
            elif analysis_type == AnalysisType.VISUALIZATION:
                result += "**Visualization Analysis:**\n"
                result += "The following visualizations were generated:\n"
                result += "- Distribution histogram\n"
                result += "- Correlation plot\n"
                result += "- Box plot of numeric variables\n"
            
            return result
            
        except Exception as e:
            return f"Error analyzing data: {str(e)}"
    
    def _generate_general_analysis(self, query: str, analysis_type: AnalysisType) -> str:
        """Generates general analysis without specific data."""
        result = f"General analysis based on query: '{query}'\n\n"
        result += f"Analysis type: {analysis_type.value}\n\n"
        
        if analysis_type == AnalysisType.EXPLORATORY:
            result += "For a complete exploratory analysis, you would need to load a dataset. "
            result += "You can upload a CSV, JSON or Excel file to get started."
            
        elif analysis_type == AnalysisType.STATISTICAL:
            result += "For statistical analysis, you would need numeric data. "
            result += "Consider loading a dataset with quantitative variables."
            
        elif analysis_type == AnalysisType.PREDICTION:
            result += "For predictions, you would need historical data. "
            result += "Specify which variable you want to predict and what features to use."
            
        return result
    
    async def _load_data(self, data_source_id: str) -> Optional[pd.DataFrame]:
        """Loads data from a source with Redis caching."""
        try:
            cache_key = self._get_cache_key("data", data_source_id)
            cached_data = self._cache_get(cache_key)
            if cached_data is not None:
                return cached_data
            
            data_source = self.data_sources.get(data_source_id)
            if not data_source:
                return None
            
            # Load data according to type
            if data_source.file_path:
                if data_source.file_path.endswith('.csv'):
                    df = pd.read_csv(data_source.file_path)
                elif data_source.file_path.endswith('.json'):
                    df = pd.read_json(data_source.file_path)
                elif data_source.file_path.endswith('.xlsx'):
                    df = pd.read_excel(data_source.file_path)
                else:
                    logger.error(f"Unsupported file type: {data_source.file_path}")
                    return None
                
                # Cache data with Redis
                self._cache_set(cache_key, df, expire=7200)  # 2 hours cache
                return df
            
            return None
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None
    
    async def _broadcast_analysis_result(self, response: DataAnalysisResponse):
        """Sends analysis result via WebSocket."""
        try:
            ws_message = WebSocketDataMessage(
                type="analysis_result",
                data={
                    "analysis_id": response.id,
                    "query": response.query,
                    "result": response.result,
                    "analysis_type": response.analysis_type.value,
                    "processing_time": response.processing_time,
                    "timestamp": response.timestamp.isoformat()
                }
            )
            
            await manager.broadcast_to_channel(
                ws_message.dict(),
                "data"
            )
            
        except Exception as e:
            logger.error(f"Error sending result via WebSocket: {e}")
    
    def add_data_source(self, data_source: DataSource) -> str:
        """Adds a new data source with Redis caching."""
        data_source.id = str(uuid.uuid4())
        
        # Store in Redis cache
        cache_key = self._get_cache_key("source", data_source.id)
        self._cache_set(cache_key, data_source.dict(), expire=86400)  # 24 hours
        
        # Also keep in memory for backward compatibility
        self.data_sources[data_source.id] = data_source
        return data_source.id
    
    def get_data_source(self, data_source_id: str) -> Optional[DataSource]:
        """Gets a data source from cache or memory."""
        # Try Redis cache first
        cache_key = self._get_cache_key("source", data_source_id)
        cached_source = self._cache_get(cache_key)
        if cached_source:
            return DataSource(**cached_source)
        
        # Fallback to memory
        return self.data_sources.get(data_source_id)
    
    def get_data_sources(self) -> List[DataSource]:
        """Gets all data sources from cache and memory."""
        sources = []
        
        # Get from memory (backward compatibility)
        sources.extend(list(self.data_sources.values()))
        
        # Note: For full Redis implementation, you'd need to scan Redis keys
        # This is a simplified version that maintains compatibility
        
        return sources
    
    def get_analysis_history(self, user_id: Optional[int] = None) -> List[DataAnalysisResponse]:
        """Gets analysis history."""
        analyses = list(self.analyses.values())
        
        if user_id:
            analyses = [a for a in analyses if a.metadata and a.metadata.get("user_id") == user_id]
        
        # Sort by timestamp (most recent first)
        analyses.sort(key=lambda x: x.timestamp, reverse=True)
        return analyses
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Gets analysis statistics."""
        total_analyses = len(self.analyses)
        total_data_sources = len(self.data_sources)
        
        analysis_types = {}
        for analysis in self.analyses.values():
            analysis_type = analysis.analysis_type.value
            analysis_types[analysis_type] = analysis_types.get(analysis_type, 0) + 1
        
        return {
            "total_analyses": total_analyses,
            "total_data_sources": total_data_sources,
            "analysis_types": analysis_types,
            "average_processing_time": sum(a.processing_time or 0 for a in self.analyses.values()) / total_analyses if total_analyses > 0 else 0
        }

# Global instance of data service
data_service = DataService()
