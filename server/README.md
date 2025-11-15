# RhinoCommon MCP 서버

Claude Code와 통신하는 MCP 서버입니다.

## 기능

- **search_rhinocommon**: API 검색
- **get_class_details**: 클래스 상세 정보
- **get_code_examples**: 코드 예제

## 설치

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. Claude Desktop 설정

#### Mac

```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### Windows

```bash
notepad %APPDATA%\Claude\claude_desktop_config.json
```

설정 내용:

```json
{
  "mcpServers": {
    "rhinocommon": {
      "command": "python",
      "args": ["/절대/경로/rhinocommon-mcp/server/mcp_server.py"]
    }
  }
}
```

### 3. Claude Code 재시작

## 테스트

```bash
# 서버 직접 실행 (테스트용)
python mcp_server.py

# 정상 작동하면 stdio로 통신 대기 상태가 됩니다
```

## 설정

`config.py`에서:
- 문서 경로
- 캐시 설정
- 로깅 레벨