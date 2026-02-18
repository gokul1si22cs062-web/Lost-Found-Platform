"""
Pre-flight check script to verify environment setup before running the server.
"""
import sys
import os
import subprocess

# Add site-packages to path (for D:\python.exe installation)
site_packages = r'D:\Lib\site-packages'
if os.path.exists(site_packages) and site_packages not in sys.path:
    sys.path.insert(0, site_packages)

def check_python_version():
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_dependencies():
    print("\nChecking dependencies...")
    required = [
        "fastapi",
        "uvicorn",
        "motor",
        "pydantic",
        "pymongo"
    ]
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    return True

def check_mongodb_connection():
    print("\nChecking MongoDB connection...")
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        import os
        from dotenv import load_dotenv
        import asyncio
        
        load_dotenv()
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        
        async def test_connection():
            try:
                client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=2000)
                await client.admin.command('ping')
                return True
            except Exception as e:
                print(f"✗ Cannot connect to MongoDB: {e}")
                print(f"  Connection string: {mongodb_url}")
                print("\n  Options:")
                print("  1. Make sure MongoDB is running locally")
                print("  2. Or set MONGODB_URL in .env file for MongoDB Atlas")
                return False
        
        result = asyncio.run(test_connection())
        if result:
            print("✓ MongoDB connection successful")
        return result
    except Exception as e:
        print(f"✗ Error checking MongoDB: {e}")
        return False

def main():
    print("="*60)
    print("LOST & FOUND PLATFORM - SETUP VERIFICATION")
    print("="*60)
    
    checks = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "MongoDB Connection": check_mongodb_connection()
    }
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {check_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to run the server.")
        print("\nNext steps:")
        print("  1. Start the server: uvicorn main:app --reload")
        print("  2. Open API docs: http://localhost:8000/docs")
        print("  3. Run tests: python test_api.py")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
    
    return all_passed

if __name__ == "__main__":
    main()

