#!/bin/bash

set -e

echo "🚀 RhinoCommon MCP 설정 시작..."

# 1. 가상환경 생성
echo "📦 가상환경 생성..."
python3 -m venv venv
source venv/bin/activate

# 2. 의존성 설치
echo "📥 의존성 설치..."
pip install -r requirements.txt
pip install -r scraper/requirements.txt
pip install -r server/requirements.txt

# 3. 디렉토리 생성
echo "📁 디렉토리 생성..."
mkdir -p docs/v8
mkdir -p docs/v7
mkdir -p docs/markdown
mkdir -p docs/examples

echo "✅ 설정 완료!"
echo ""
echo "다음 단계:"
echo "1. cd scraper && python scraper.py --version 8"
echo "2. cd ../server && ./scripts/install_mcp.sh"