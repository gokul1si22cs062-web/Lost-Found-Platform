"""
Start the FastAPI server with proper path setup
"""
import sys
import os

# Add site-packages to path
site_packages = r'D:\Lib\site-packages'
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)

# Now import and run
try:
    import uvicorn
    from main import app
    
    print("=" * 60)
    print("Starting Lost & Found Platform API Server")
    print("=" * 60)
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("\nMake sure all dependencies are installed:")
    print("  py install_packages.py")
    sys.exit(1)
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

