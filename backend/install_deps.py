"""
Install dependencies using subprocess
"""
import subprocess
import sys

packages = [
    "fastapi",
    "uvicorn[standard]",
    "motor",
    "pydantic",
    "python-dotenv",
    "python-multipart",
    "requests"
]

print("Installing dependencies...")
print("=" * 60)

for package in packages:
    print(f"\nInstalling {package}...")
    try:
        # Try using pip through subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ {package} installed successfully")
        else:
            print(f"✗ Failed to install {package}")
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"✗ Error installing {package}: {e}")

print("\n" + "=" * 60)
print("Installation complete!")
print("\nTry running: py -m pip list")
print("If packages are installed, you can start the server with:")
print("  py -m uvicorn main:app --reload")

