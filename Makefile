# -------- Python / venv --------
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# -------- OS detection --------
UNAME_S := $(shell uname -s)

# -------- Default target --------
.PHONY: all deps venv install clean
all: deps venv install

# -------- System dependencies --------
deps:
ifeq ($(UNAME_S), Linux)
	@echo "Detected Linux..."
	@if command -v apt >/dev/null 2>&1; then \
		echo "Using apt (Ubuntu/Debian/Raspberry Pi)..."; \
		sudo apt update && sudo apt install -y \
			python3-dev \
			python3-venv \
			portaudio19-dev; \
	elif command -v dnf >/dev/null 2>&1; then \
		echo "Using dnf (Fedora)..."; \
		sudo dnf install -y python3-devel portaudio-devel; \
	elif command -v pacman >/dev/null 2>&1; then \
		echo "Using pacman (Arch)..."; \
		sudo pacman -Sy --noconfirm python portaudio; \
	else \
		echo "Unsupported Linux distribution. Install PortAudio manually."; \
	fi
else ifeq ($(UNAME_S), Darwin)
	@echo "Detected macOS..."
	brew install portaudio
else
	@echo "Unsupported OS ($(UNAME_S))."
	@echo "Windows: install PortAudio and PyAudio manually."
endif

# -------- Virtual environment --------
venv:
	@test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools wheel

# -------- Python dependencies --------
install: venv
	$(PIP) install -r requirements.txt

# -------- Cleanup --------
clean:
	rm -rf $(VENV) __pycache__ .pytest_cache build dist *.egg-info
