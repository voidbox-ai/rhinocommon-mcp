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

## 🐳 Docker로 시작하기 (권장)

### 1단계: Docker 컨테이너 실행

```bash
# 저장소 클론
git clone https://github.com/voidbox-ai/rhinocommon-mcp.git
cd rhinocommon-mcp

# 문서 크롤링 및 서버 실행
docker-compose up -d
```

컨테이너 상태 확인:
```bash
docker ps
# rhinocommon-mcp-server와 rhinocommon-scraper가 실행 중이어야 함
```

문서 데이터 확인:
```bash
ls docs/v8
# RhinoCommon API 문서 JSON 파일들이 있어야 함
```

### 2단계: MCP 서버 등록

#### VSCode Claude Code 사용자

1. VSCode 설정 열기: `Cmd + Shift + P` → "Preferences: Open User Settings (JSON)"
2. 다음 설정 추가:

```json
{
  "claude.mcpServers": {
    "rhinocommon": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "rhinocommon-mcp-server",
        "python",
        "/app/server/mcp_server.py"
      ]
    }
  }
}
```

3. VSCode 재시작

#### Claude Desktop 사용자

설정 파일 경로:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

설정 내용:
```json
{
  "mcpServers": {
    "rhinocommon": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "rhinocommon-mcp-server",
        "python",
        "/app/server/mcp_server.py"
      ]
    }
  }
}
```

Claude Desktop 재시작

### 3단계: 연결 테스트

Claude에서 다음과 같이 테스트:

```
"RhinoCommon에서 Point3d 클래스 정보 알려줘"
```

Claude가 `search_rhinocommon`과 `get_class_details` 도구를 자동으로 사용하면 성공입니다!

## 📚 사용 예시

### 예시 1: 클래스 검색

**사용자**: "RhinoCommon으로 NURBS 곡면을 생성하는 코드 작성해줘"

**Claude 동작**:
1. `search_rhinocommon("NurbsSurface")` 호출 → 관련 클래스 검색
2. `get_class_details("NurbsSurface")` 호출 → 상세 API 문서 조회
3. 정확한 생성자, 메서드, 속성 정보를 기반으로 코드 작성

### 예시 2: 특정 메서드 사용

**사용자**: "Brep Boolean 연산 코드 작성해줘"

**Claude 동작**:
1. `search_rhinocommon("Brep Boolean")` 호출
2. `get_class_details("Brep")` 호출
3. `get_code_examples("Brep")` 호출
4. Boolean 연산 메서드를 정확하게 사용한 코드 작성

### 제공되는 MCP 도구

- **`search_rhinocommon`**: 클래스/메서드 이름으로 검색
- **`get_class_details`**: 클래스의 모든 메서드, 속성, 생성자 정보 조회
- **`get_code_examples`**: 실제 코드 예제 조회

## 🔧 로컬 설치 (Docker 없이)

### Python 환경 설정

```bash
# 문서 크롤링
cd scraper
pip install -r requirements.txt
python scraper.py --version 8

# 서버 설치
cd ../server
pip install -r requirements.txt
```

### MCP 서버 등록 (로컬)

**VSCode**:
```json
{
  "claude.mcpServers": {
    "rhinocommon": {
      "command": "python",
      "args": ["/절대/경로/rhinocommon-mcp/server/mcp_server.py"]
    }
  }
}
```

**Claude Desktop**:
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