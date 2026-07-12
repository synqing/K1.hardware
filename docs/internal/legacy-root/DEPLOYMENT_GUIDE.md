# Deployment Guide

This guide provides instructions on how to set up the necessary environment to run the K1 Lightwave PCB design automation tool.

## 1. Install KiCad

The core of this automation tool relies on KiCad's Python API (`pcbnew`). Therefore, a full installation of KiCad is required.

**macOS:**

```bash
brew install kicad
```

**Linux (Ubuntu/Debian):**

```bash
sudo add-apt-repository --yes ppa:kicad/kicad-7.0-releases
sudo apt-get update
sudo apt-get install -y kicad
```

**Windows:**

Download and install KiCad from the official website: [https://www.kicad.org/download/](https://www.kicad.org/download/)

## 2. Verify KiCad Installation

After installing KiCad, verify that the `kicad-cli` command-line tool is available in your system's PATH. Open a new terminal and run:

```bash
kicad-cli --version
```

You should see an output displaying the KiCad version number.

## 3. Install Python Dependencies

The project requires several Python packages to be installed. These can be installed using `pip`:

```bash
pip install -r mcp/mcp-rag/requirements.txt
pip install skidl
```

## 4. Configure the Environment

Once the dependencies are installed, run the configuration script to set up the local servers for the Claude Code agent:

```bash
python3 mcp/configure_claude.py
```

This script will automatically detect your KiCad installation and generate the necessary configuration files.

## 5. Verify the Setup

After running the configuration script, verify that the environment is correctly set up by running the verification script:

```bash
python3 mcp/verify-servers.py
```

If all checks pass, you are ready to start designing PCBs.
