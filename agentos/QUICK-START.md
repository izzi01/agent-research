# 🚀 QUICK START - Vietnamese Marketing Automation

## ⚡ Why UV?

**UV is the blazing-fast Python package manager written in Rust**

- Installing dependencies: **30 seconds** 
- Creating virtual environments: **Instant**
- Resolving dependencies: **Lightning fast**
- 10-100x faster than traditional methods

---

## 🎯 FASTEST PATH TO RUNNING (2 Minutes!)

### **One-Command Startup:**

```bash
cd /home/cid/projects-personal/agent-research/agentos
./start.sh
```

This will:
1. ✅ Check Python version
2. ✅ Install UV if not present
3. ✅ Create virtual environment (`.venv`)
4. ✅ Install all dependencies in ~30 seconds
5. ✅ Ask if you want to run test script

---

## 📋 MANUAL SETUP (Step-by-Step)

### **Step 1: Create Virtual Environment**

```bash
cd /home/cid/projects-personal/agent-research/agentos

# Create venv with UV (instant!)
uv venv .venv

# Activate it
source .venv/bin/activate
```

**Time:** <1 second

---

### **Step 2: Install Dependencies**

```bash
# Install with UV
uv pip install -r requirements.txt
```

**Time:** ~30 seconds

**You'll see:**
```
Resolved 48 packages in 2s
Downloaded 48 packages in 15s
Installed 48 packages in 10s
```

---

### **Step 3: Test Immediately**

```bash
# Run test with mock data (no API keys needed)
python test_textcreator.py
```

**Expected Output:**
```
==============================================================
📱 FACEBOOK COPY
==============================================================

Variant: default | Tone: casual

Hôm nay mình review cho các bạn cây son lì này nha! 💄
...
```

✅ **Done! You just went from zero to running in under 2 minutes!**

---

## 🔧 UV COMMANDS CHEATSHEET

### **Virtual Environment:**
```bash
# Create venv
uv venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Deactivate
deactivate
```

### **Package Management:**
```bash
# Install from requirements.txt
uv pip install -r requirements.txt

# Install single package
uv pip install agno

# Install with version
uv pip install "agno==0.3.2"

# Install development dependencies
uv pip install pytest black flake8

# List installed packages
uv pip list

# Show package info
uv pip show agno

# Uninstall package
uv pip uninstall agno
```

### **Advanced Features:**
```bash
# UV Sync (if you have pyproject.toml)
uv sync

# UV Run (run without activating venv)
uv run python test_textcreator.py

# Show cache directory
uv cache dir

# Clear cache
uv cache clean
```

---

## 🎯 FULL SETUP (30 Seconds)

### **Complete Installation:**

```bash
# 1. Navigate to project
cd /home/cid/projects-personal/agent-research/agentos

# 2. Create venv + install deps in ONE command
uv venv .venv && source .venv/bin/activate && uv pip install -r requirements.txt

# 3. Test immediately
python test_textcreator.py
```

**Total time:** ~30-40 seconds ⚡

---

## 🚀 RECOMMENDED WORKFLOW

### **Day 1: Initial Setup (30 seconds)**

```bash
cd /home/cid/projects-personal/agent-research/agentos
./start.sh
# Choose 'y' to run test
```

✅ **See Vietnamese content generated immediately!**

---

### **Day 2: Development Workflow**

```bash
# Activate venv (if not activated)
source .venv/bin/activate

# Install new package (lightning fast!)
uv pip install new-package

# Run tests
python test_textcreator.py

# Start server
python main.py
```

---

### **Day 3: Add Dependencies**

```bash
# Install and add to requirements
uv pip install httpx

# Freeze current environment
uv pip freeze > requirements.txt
```

---

## 💡 UV TIPS & TRICKS

### **1. Automatic Virtual Environment Activation**

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Auto-activate .venv when entering directory
cd() {
  builtin cd "$@"
  if [[ -d .venv ]]; then
    source .venv/bin/activate
  fi
}
```

### **2. UV with Docker**

```dockerfile
# In your Dockerfile
FROM python:3.12-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies with UV
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Much faster Docker builds!
```

---

## 🆘 TROUBLESHOOTING

### **"uv: command not found"**

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Verify
uv --version
```

### **"Virtual environment not found"**

```bash
# Create it
uv venv .venv

# Activate
source .venv/bin/activate
```

### **"Package not found in index"**

```bash
# Install from URL
uv pip install git+https://github.com/user/repo.git

# Or from local path
uv pip install -e /path/to/package
```

---

## 🎯 YOUR NEXT ACTION

**Run this command RIGHT NOW:**

```bash
cd /home/cid/projects-personal/agent-research/agentos
./start.sh
```

**What happens:**
1. ⚡ Creates venv in <1 second
2. ⚡ Installs 48 packages in ~30 seconds
3. 🧪 Runs test and shows Vietnamese content
4. ✅ You're ready to develop!

**Total time:** ~1-2 minutes

---

## 📚 UV RESOURCES

- **Official Docs:** https://docs.astral.sh/uv/
- **GitHub:** https://github.com/astral-sh/uv
- **Installation:** https://astral.sh/uv/install.sh
- **Comparison:** See `UV-VS-PIP.md` for detailed benchmarks

---

**Ready?** Run `./start.sh` and experience the speed! ⚡🚀
