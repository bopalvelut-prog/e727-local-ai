#!/bin/bash
# Quick wrapper for LLM Autochooser

cd /home/ma/e727-local-ai
source venv/bin/activate 2>/dev/null

python3 -m src.llm_autochooser "$@"
