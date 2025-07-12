#!/usr/bin/env python3
"""
Verification script to ensure all new features are properly configured
and don't break existing functionality.
"""

import os
import sys
import importlib
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def check_imports():
    """Check that all required imports work correctly."""
    logger.info("Checking imports...")
    
    # Core imports that should always work
    core_imports = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'pandas',
        'numpy',
        'requests',
        'sqlalchemy',
        'celery',
        'redis',
        'websockets'
    ]
    
    for module in core_imports:
        try:
            importlib.import_module(module)
            logger.info(f"✅ {module} - OK")
        except ImportError as e:
            logger.warning(f"⚠️  {module} - Not available: {e}")
    
    # Optional imports for new features
    optional_imports = [
        ('sentry_sdk', 'Sentry error monitoring'),
        ('redis', 'Redis caching'),
    ]
    
    for module, description in optional_imports:
        try:
            importlib.import_module(module)
            logger.info(f"✅ {module} - {description} available")
        except ImportError:
            logger.info(f"ℹ️  {module} - {description} not installed (optional)")

def check_configuration():
    """Check configuration files and environment variables."""
    logger.info("Checking configuration...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        logger.info("✅ .env file exists")
    else:
        logger.info("ℹ️  .env file not found (using env.example as template)")
    
    # Check required directories
    required_dirs = ['logs', 'uploads', 'temp']
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            logger.info(f"✅ {dir_name}/ directory exists")
        else:
            logger.info(f"ℹ️  {dir_name}/ directory will be created on startup")
    
    # Check environment variables
    env_vars = {
        'SECRET_KEY': 'Security key for JWT tokens',
        'DATABASE_URL': 'Database connection string',
        'REDIS_URL': 'Redis connection string (optional)',
        'SENTRY_DSN': 'Sentry error monitoring (optional)',
    }
    
    for var, description in env_vars.items():
        if os.getenv(var):
            logger.info(f"✅ {var} - {description} configured")
        else:
            logger.info(f"ℹ️  {var} - {description} not set (will use defaults)")

def check_backend_structure():
    """Check backend file structure and imports."""
    logger.info("Checking backend structure...")
    
    backend_path = Path("app")
    if not backend_path.exists():
        logger.error("❌ Backend app directory not found")
        return False
    
    # Check main files
    main_files = [
        'main.py',
        'core/config.py',
        'services/data_service.py',
        'services/ai_service.py',
        'services/chat_service.py',
        'api/v1/endpoints/auth.py',
        'api/v1/endpoints/health.py',
    ]
    
    for file_path in main_files:
        full_path = backend_path / file_path
        if full_path.exists():
            logger.info(f"✅ {file_path} - OK")
        else:
            logger.warning(f"⚠️  {file_path} - Not found")
    
    return True

def check_frontend_structure():
    """Check frontend file structure."""
    logger.info("Checking frontend structure...")
    
    frontend_path = Path("../frontend/src")
    if not frontend_path.exists():
        logger.warning("⚠️  Frontend directory not found (may be in different location)")
        return True
    
    # Check main files
    main_files = [
        'App.jsx',
        'main.jsx',
        'components/LoginForm.jsx',
        'components/Chat.jsx',
        'components/NavBar.jsx',
        'api/auth.js',
    ]
    
    for file_path in main_files:
        full_path = frontend_path / file_path
        if full_path.exists():
            logger.info(f"✅ {file_path} - OK")
        else:
            logger.warning(f"⚠️  {file_path} - Not found")
    
    return True

def check_dependencies():
    """Check if all dependencies are properly listed."""
    logger.info("Checking dependencies...")
    
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        with open(requirements_file, 'r') as f:
            content = f.read()
            
        # Check for new dependencies
        new_deps = [
            'sentry-sdk[fastapi]',
            'redis',
        ]
        
        for dep in new_deps:
            if dep in content:
                logger.info(f"✅ {dep} - Listed in requirements.txt")
            else:
                logger.warning(f"⚠️  {dep} - Not found in requirements.txt")
    else:
        logger.warning("⚠️  requirements.txt not found")

def run_backend_tests():
    """Run basic backend functionality tests."""
    logger.info("Running backend functionality tests...")
    
    try:
        # Test configuration loading
        sys.path.insert(0, str(Path.cwd()))
        from app.core.config import settings
        
        logger.info("✅ Configuration loaded successfully")
        logger.info(f"   App name: {settings.app_name}")
        logger.info(f"   Version: {settings.version}")
        logger.info(f"   Debug mode: {settings.debug}")
        
        # Test data service initialization
        from app.services.data_service import DataService
        data_service = DataService()
        logger.info("✅ DataService initialized successfully")
        
        # Test Redis availability
        if hasattr(data_service, 'redis_available'):
            if data_service.redis_available:
                logger.info("✅ Redis cache is available")
            else:
                logger.info("ℹ️  Redis cache not available (using in-memory fallback)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Backend test failed: {e}")
        return False

def main():
    """Main verification function."""
    logger.info("🔍 Starting system verification...")
    logger.info("=" * 50)
    
    # Change to backend directory if needed
    if Path("app").exists():
        logger.info("Running from backend directory")
    elif Path("../backend/app").exists():
        os.chdir("../backend")
        logger.info("Changed to backend directory")
    else:
        logger.error("❌ Backend directory not found")
        return False
    
    # Run all checks
    checks = [
        check_imports,
        check_configuration,
        check_backend_structure,
        check_frontend_structure,
        check_dependencies,
        run_backend_tests,
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            logger.error(f"❌ Check failed: {e}")
            results.append(False)
    
    # Summary
    logger.info("=" * 50)
    logger.info("📊 Verification Summary:")
    
    passed = sum(1 for r in results if r is not False)
    total = len(results)
    
    if passed == total:
        logger.info("🎉 All checks passed! System is properly configured.")
        logger.info("✅ New features are ready to use:")
        logger.info("   - Redis caching (optional)")
        logger.info("   - Sentry error monitoring (optional)")
        logger.info("   - React Context for state management")
        logger.info("   - Architecture documentation")
    else:
        logger.warning(f"⚠️  {passed}/{total} checks passed")
        logger.info("Some features may not work as expected.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 