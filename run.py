"""
Spark Intelligence Copilot - Main entry point

Run this script to start the application locally.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import uvicorn
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get configuration
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"""
    ╔══════════════════════════════════════════════╗
    ║   Spark Intelligence Copilot                 ║
    ║   Starting API Server...                     ║
    ╚══════════════════════════════════════════════╝
    
    Host: {host}
    Port: {port}
    Auto Reload: {reload}
    
    API Docs: http://{host}:{port}/docs
    """)
    
    # Start the application
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
