# RhinoCommon 문서 크롤러

RhinoCommon API 문서를 수집하고 구조화합니다.

## 기능

- **XML 파싱**: Rhino SDK의 XML 문서 파싱 (가장 정확)
- **웹 스크래핑**: 온라인 API 문서 크롤링
- **다중 버전 지원**: Rhino 7, 8 등 여러 버전 지원

## 사용법

### 1. XML 파싱 (권장)

```bash
# Rhino 8 XML 문서 파싱
python scraper.py --source xml --path "/path/to/RhinoCommon.xml" --version 8

# Windows
python scraper.py --source xml --path "C:\Program Files\Rhino 8\System\RhinoCommon.xml"

# Mac
python scraper.py --source xml --path "/Applications/Rhino 8.app/Contents/Frameworks/RhinoCommon.xml"
```

### 2. 웹 스크래핑

```bash
# 온라인 문서 크롤링
python scraper.py --source web --version 8

# 특정 네임스페이스만
python scraper.py --source web --namespace rhino.geometry
```

### 3. 전체 수집

```bash
# 모든 네임스페이스 수집
python scraper.py --all --version 8
```

## 출력

수집된 문서는 `../docs/v8/` 디렉토리에 저장됩니다:
- `index.json`: 전체 인덱스
- `rhino_geometry.json`: Rhino.Geometry 네임스페이스
- `rhino_docobjects.json`: Rhino.DocObjects 네임스페이스
- ...

## 설정

`config.py`에서 다음을 설정할 수 있습니다:
- 크롤링 딜레이
- 네임스페이스 목록
- 출력 경로