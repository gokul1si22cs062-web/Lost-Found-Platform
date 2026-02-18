"""
Install packages by adding site-packages to path first
"""
import sys
import os

# Add the site-packages to path
site_packages = r'D:\Lib\site-packages'
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)

# Now try to import and use pip
try:
    import pip._internal.main as pip_main
    packages = [
        'fastapi',
        'uvicorn[standard]',
        'motor',
        'pydantic',
        'python-dotenv',
        'python-multipart',
        'requests'
    ]
    
    print("Installing packages...")
    for package in packages:
        print(f"\nInstalling {package}...")
        pip_main.main(['install', package])
    print("\n✓ All packages installed!")
    
except ImportError:
    # Try using subprocess with pip module
    import subprocess
    import site
    
    # Add site-packages to environment
    env = os.environ.copy()
    pythonpath = env.get('PYTHONPATH', '')
    if site_packages not in pythonpath:
        env['PYTHONPATH'] = f"{site_packages};{pythonpath}" if pythonpath else site_packages
    
    packages = [
        'fastapi',
        'uvicorn[standard]',
        'motor',
        'pydantic',
        'python-dotenv',
        'python-multipart',
        'requests'
    ]
    
    print("Installing packages using subprocess...")
    for package in packages:
        print(f"\nInstalling {package}...")
        result = subprocess.run(
            [sys.executable, '-c', f'import sys; sys.path.insert(0, r"{site_packages}"); import pip._internal.main; pip._internal.main.main(["install", "{package}"])'],
            env=env
        )
        if result.returncode == 0:
            print(f"✓ {package} installed")
        else:
            print(f"✗ Failed to install {package}")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative method...")
    
    # Last resort: use pip.exe directly if it exists
    pip_exe = r'D:\Scripts\pip.exe'
    if os.path.exists(pip_exe):
        import subprocess
        packages = 'fastapi uvicorn[standard] motor pydantic python-dotenv python-multipart requests'
        subprocess.run([pip_exe, 'install'] + packages.split())
    else:
        print("Could not install packages automatically.")
        print("Please run manually:")
        print(f"  {sys.executable} -m pip install fastapi uvicorn motor pydantic python-dotenv python-multipart requests")

