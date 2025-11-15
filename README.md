# rhinocommon-mcp
Rhinocommon API mcp for Rhino plugin developers

Claude Code에서 Rhino 8 RhinoCommon API 문서를 참조할 수 있게 해주는 MCP(Model Context Protocol) 서버입니다.

## 🎯 목적

Rhino 플러그인 개발 시 Claude Code가 정확한 RhinoCommon API를 참조하여 코드를 생성하도록 돕습니다.

## ⚡ 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/voidbox-ai/rhinocommon-mcp.git
cd rhinocommon-mcp
```

### 2. 문서 수집

```bash
cd scraper
pip install -r requirements.txt
python scraper.py --version 8
```

### 3. MCP 서버 설치

```bash
cd ../server
pip install -r requirements.txt

# Claude Code 설정
./scripts/install_mcp.sh
```

### 4. Claude Code 재시작

설정이 완료되면 Claude Code를 재시작하세요.

## 📁 프로젝트 구조

- `/scraper` - RhinoCommon 문서 크롤러
- `/server` - MCP 서버
- `/docs` - 수집된 문서 데이터
- `/scripts` - 유틸리티 스크립트

자세한 내용은 각 디렉토리의 README.md를 참조하세요.

## 🐳 Docker 사용

```bash
# 전체 빌드 및 실행
docker-compose up -d

# 크롤러만 실행
docker-compose run scraper

# 서버만 실행
docker-compose up server
```

## 📚 사용 예시

Claude Code에서:
```
사용자: "RhinoCommon으로 NURBS 곡면을 생성하는 코드 작성해줘"

Claude: search_rhinocommon("NurbsSurface") 호출
        get_class_details("NurbsSurface") 호출
        정확한 API 문서를 기반으로 코드 작성
```

## 🔧 설정

### Claude Desktop 설정

`~/Library/Application Support/Claude/claude_desktop_config.json` (Mac)
`%APPDATA%\Claude\claude_desktop_config.json` (Windows)

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

## 📄 라이선스

Apache 2.0 License

## 🔗 관련 링크

- [RhinoCommon API Reference](https://mcneel-apidocs.herokuapp.com/api/rhinocommon/)
- [Rhino Developer Docs](https://developer.rhino3d.com/)
- [MCP Protocol](https://modelcontextprotocol.io/)