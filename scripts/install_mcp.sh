#!/bin/bash

set -e

# 현재 디렉토리의 절대 경로
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SERVER_PATH="$PROJECT_ROOT/server/mcp_server.py"

echo "🔧 MCP 서버 설치 중..."

# OS 감지
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_PATH="$HOME/.config/Claude/claude_desktop_config.json"
else
    echo "❌ 지원하지 않는 OS입니다."
    exit 1
fi

# 설정 파일 디렉토리 생성
mkdir -p "$(dirname "$CONFIG_PATH")"

# 기존 설정 백업
if [ -f "$CONFIG_PATH" ]; then
    cp "$CONFIG_PATH" "$CONFIG_PATH.backup"
    echo "📋 기존 설정 백업: $CONFIG_PATH.backup"
fi

# 설정 생성/업데이트
cat > "$CONFIG_PATH" << EOF
{
  "mcpServers": {
    "rhinocommon": {
      "command": "python",
      "args": ["$SERVER_PATH"]
    }
  }
}
EOF

echo "✅ MCP 서버 설치 완료!"
echo "📍 설정 파일: $CONFIG_PATH"
echo "📍 서버 경로: $SERVER_PATH"
echo ""
echo "⚠️  Claude Code를 재시작해주세요."