# Installation Guide - Fixing Python/Pip Issues

## Current Issue

Your Python installation at `D:\python.exe` doesn't have pip properly configured. Here are solutions:

## Solution 1: Reinstall Python (Recommended)

1. **Download Python from python.org:**
   - Go to: https://www.python.org/downloads/
   - Download Python 3.11 or 3.12 (stable versions)
   - **IMPORTANT:** During installation, check "Add Python to PATH"

2. **After installation, verify:**
   ```powershell
   python --version
   pip --version
   ```

3. **Install dependencies:**
   ```powershell
   cd "D:\internship project\Lost-Found-Platform-1\backend"
   pip install -r requirements.txt
   ```

## Solution 2: Use Python from Microsoft Store

1. **Install Python from Microsoft Store:**
   - Open Microsoft Store
   - Search for "Python 3.11" or "Python 3.12"
   - Install it

2. **After installation:**
   ```powershell
   python --version
   pip install -r requirements.txt
   ```

## Solution 3: Use Virtual Environment (Best Practice)

1. **Install Python properly** (from Solution 1 or 2)

2. **Create virtual environment:**
   ```powershell
   cd "D:\internship project\Lost-Found-Platform-1\backend"
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```powershell
   # Windows PowerShell
   venv\Scripts\Activate.ps1
   
   # Or Windows CMD
   venv\Scripts\activate.bat
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run server:**
   ```powershell
   python -m uvicorn main:app --reload
   ```

## Solution 4: Manual Package Installation

If pip still doesn't work, you can manually download and install packages:

1. **Download wheels from PyPI:**
   - Visit: https://pypi.org/
   - Search for each package and download the `.whl` file
   - Install using: `python -m pip install package.whl`

2. **Or use conda (if you have Anaconda/Miniconda):**
   ```powershell
   conda install fastapi uvicorn motor pydantic python-dotenv requests
   ```

## Quick Fix: Add D:\Scripts to PATH

If pip is installed in `D:\Scripts` but not accessible:

1. **Temporarily (this session):**
   ```powershell
   $env:PATH += ";D:\Scripts"
   pip install -r requirements.txt
   ```

2. **Permanently:**
   - Open System Properties → Environment Variables
   - Add `D:\Scripts` to PATH
   - Restart terminal

## After Installation

Once dependencies are installed:

1. **Verify installation:**
   ```powershell
   python verify_setup.py
   ```

2. **Start server:**
   ```powershell
   python -m uvicorn main:app --reload
   ```

3. **Test API:**
   - Open: http://localhost:8000/docs
   - Or run: `python test_api.py`

## Troubleshooting

### "Python was not found"
- Install Python from python.org
- Make sure to check "Add Python to PATH" during installation

### "No module named pip"
- Run: `python -m ensurepip --upgrade`
- Or reinstall Python with pip included

### "Permission denied"
- Run PowerShell as Administrator
- Or use `--user` flag: `pip install --user -r requirements.txt`

### Port 8000 already in use
- Change port: `uvicorn main:app --reload --port 8001`

## Recommended Setup

For best results, use **Solution 3 (Virtual Environment)**:

```powershell
# 1. Create venv
python -m venv venv

# 2. Activate
venv\Scripts\Activate.ps1

# 3. Install
pip install -r requirements.txt

# 4. Run
python -m uvicorn main:app --reload
```

This isolates your project dependencies and avoids system-wide conflicts.

