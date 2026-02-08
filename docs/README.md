# Intelligence Agent - 보안 블로그 자동화

보안 뉴스를 자동으로 수집하고, LLM으로 블로그 글을 작성하여 Hugo 블로그에 자동 배포하는 시스템입니다.

---

## 📋 목차

1. [개요](#개요)
2. [워크플로우](#워크플로우)
3. [설치](#설치)
4. [사용법](#사용법)
5. [모듈 설명](#모듈-설명)
6. [환경변수 설정](#환경변수-설정)
7. [테스트](#테스트)

---

## 개요

Intelligence Agent는 다음 4단계 프로세스로 보안 블로그를 자동화합니다:

1. **News Collector**: RSS feeds (Google News, arXiv, HackerNews)에서 보안 관련 뉴스 수집
2. **LLM Writer**: GPT-4o를 사용하여 보안 전문가 페르소나로 전문적인 블로그 글 작성
3. **Notion Publisher**: Notion Database에 Draft 상태로 저장
4. **Git Publisher**: 사용자가 Notion에서 상태를 "Publish"로 변경하면 Git push → GitHub Actions 자동 배포

---

## 워크플로우

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌─────────────┐
│   Collector │ →    │    Analyst   │ →    │   Human UI   │ →    │   Human UI   │ →    │   Publisher │
│  (RSS/News) │      │  (LLM Writing)│     │   (Notion)   │      │   (Notion)   │      │ (Git Push)  │
└─────────────┘      └──────────────┘      └──────────────┘      └──────────────┘      └─────────────┘
      │                     │                       │                     │                     │
  Google News RSS       GPT-4o               Notion App             Notion App            Git Push
  arXiv               Security Analyst       Manual Review          Manual Approval      GitHub Actions
  HackerNews                    │                  Status Change         Status Change        Auto Deploy
                                  │                   → Draft               → Publish/        to Pages
                                  │                  (검토 완료)            승인 완료           배포 완료
                                  │
                    ┌────────────┴────────────┐
                    │        Image Pipeline    │
                    │  Download → Copy →      │
                    │   Reference in Markdown  │
                    └─────────────────────────┘
```

---

## 설치

### 1. 의존성 설치

```bash
cd /Users/nabang/Documents/OpenClaw
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일에 다음 환경변수를 추가하세요:

```bash
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Notion API
NOTION_API_KEY=your_notion_integration_token_here
NOTION_DATABASE_ID=your_notion_database_id_here

# Blog Configuration
BLOG_REPO_PATH=/Users/nabang/Documents/OpenClaw/security-blog
BLOG_URL=https://rebugui.github.io/hate-coding-turtle/
```

---

## 사용법

### 단일 실행 (테스트)

```bash
# News Collector 테스트
cd /Users/nabang/Documents/OpenClaw/modules/intelligence
python collector.py

# LLM Writer 테스트
python writer.py

# Notion Publisher 테스트
python notion_publisher.py

# Git Publisher 테스트
python publisher_git.py
```

### 전체 파이프라인 실행

```python
from modules.intelligence import NewsCollector, BlogWriter, NotionPublisher, GitPublisher

# 1. 뉴스 수집
collector = NewsCollector()
articles = collector.fetch_all(max_results_per_source=5)

# 2. 글 작성
writer = BlogWriter()
blog_posts = writer.generate_article_batch(articles)

# 3. Notion에 저장 (Draft 상태)
notion_pub = NotionPublisher()
notion_pub.create_article_batch(blog_posts)

# 4. Git Publisher 모니터링 (사용자 승인 대기)
git_pub = GitPublisher(notion_publisher=notion_pub)
git_pub.monitor_and_publish(interval_seconds=600)  # 10분마다 체크
```

---

## 모듈 설명

### 1. News Collector

RSS feeds (Google News, arXiv, HackerNews)에서 보안 관련 뉴스를 수집합니다.

**주요 기능:**
- Google News RSS 피드 수집
- arXiv 논문 수집 (CS.CR, CS.LG 카테고리)
- HackerNews 뉴스 수집
- 키워드 필터링 (Vulnerability, LLM Security, 등)
- 중복 체크

**사용 예시:**

```python
from modules.intelligence import NewsCollector

collector = NewsCollector(keywords=["Vulnerability", "LLM Security"])
articles = collector.fetch_all(max_results_per_source=10)

for article in articles:
    print(f"[{article['source']}] {article['title']}")
```

---

### 2. LLM Writer

OpenAI GPT-4o를 사용하여 보안 전문가 페르소나로 전문적인 블로그 글을 작성합니다.

**주요 기능:**
- 보안 전문가 페르소나 (10년 이상 경력)
- 전문적인 기술적 분석
- Mermaid 다이어그램 생성
- 코드 분해
- 보안 시사점 작성

**사용 예시:**

```python
from modules.intelligence import BlogWriter

writer = BlogWriter()
article_data = {
    "source": "arXiv",
    "title": "LLM Security: Adversarial Attacks",
    "url": "https://arxiv.org/abs/2401.12345",
    "published": "2024-01-15",
    "summary": "LLM 적대적 공격 분석"
}

blog_post = writer.generate_article(article_data)
print(f"제목: {blog_post['title']}")
print(f"내용: {blog_post['content']}")
```

---

### 3. Notion Publisher

Notion Database에 블로그 글을 저장하고, 상태를 "Draft"로 설정합니다.

**주요 기능:**
- Notion Database에 글 생성
- 상태 자동 설정 (Draft)
- 태그 및 카테고리 저장
- 원본 URL 및 출처 저장

**사용 예시:**

```python
from modules.intelligence import NotionPublisher

notion_pub = NotionPublisher()

article_data = {
    "title": "블로그 글 제목",
    "summary": "글 요약",
    "content": "전체 글 내용",
    "tags": ["Security", "LLM"],
    "category": "보안",
    "original_url": "https://example.com",
    "original_source": "arXiv"
}

page = notion_pub.create_article(article_data)
print(f"Page ID: {page['id']}")
```

---

### 4. Git Publisher

사용자가 Notion에서 상태를 "Publish"로 변경했을 때 Git push를 수행하여 GitHub Actions를 트리거합니다.

**주요 기능:**
- Notion 상태 모니터링 (10분 간격)
- "Publish" 상태 글 자동 배포
- Hugo 블로그 포스트 생성
- Git commit & push
- 배포 URL 업데이트
- 상태를 "Done"으로 변경

**사용 예시:**

```python
from modules.intelligence import NotionPublisher, GitPublisher

notion_pub = NotionPublisher()
git_pub = GitPublisher(notion_publisher=notion_pub)

# 대기 중인 글 배포
results = git_pub.publish_all_pending()

# 또는 상시 모니터링
git_pub.monitor_and_publish(interval_seconds=600)  # 10분마다 체크
```

---

## 환경변수 설정

### 필수 환경변수

| 환경변수 | 설명 | 예시 |
|---------|------|------|
| `OPENAI_API_KEY` | OpenAI API Key | `sk-...` |
| `NOTION_API_KEY` | Notion Integration Token | `secret_...` |
| `NOTION_DATABASE_ID` | Notion Database ID | `abc123...` |

### 선택적 환경변수

| 환경변수 | 설명 | 기본값 |
|---------|------|--------|
| `BLOG_REPO_PATH` | Hugo 블로그 저장소 경로 | `/Users/nabang/Documents/OpenClaw/security-blog` |
| `BLOG_URL` | 블로그 배포 URL | `https://rebugui.github.io/hate-coding-turtle/` |

---

## 테스트

### 단위 테스트

```bash
# Collector 테스트
python modules/intelligence/collector.py

# Writer 테스트
python modules/intelligence/writer.py

# Notion Publisher 테스트
python modules/intelligence/notion_publisher.py

# Git Publisher 테스트
python modules/intelligence/publisher_git.py
```

### 통합 테스트

```bash
# 전체 파이프라인 테스트
python scripts/test_intelligence_pipeline.py
```

---

## Human-in-the-Loop 프로세스

1. **자동 수집 & 작성**: RSS 뉴스 수집 → LLM 글 작성 → Notion Draft 저장
2. **사용자 검토**: 사용자가 Notion에서 글을 검토 및 편집
3. **사용자 승인**: 사용자가 상태를 "Publish"로 변경
4. **자동 배포**: Git Publisher가 감지 → Git push → GitHub Actions 배포

**중요**: Git Publisher는 사용자가 상태를 "Publish"로 변경했을 때만 실행됩니다. 자동으로 배포하지 않습니다.

---

## 트러블슈팅

### Notion API 에러

- **에러**: `Invalid request URL`
- **해결**: `NOTION_DATABASE_ID`가 올바른지 확인하세요.

### Git Push 실패

- **에러**: `Failed to push`
- **해결**: Git 자격증명이 설정되어 있는지 확인하세요 (`git config --global user.name`, `git config --global user.email`).

### LLM API 에러

- **에러**: `Quota exceeded`
- **해결**: OpenAI API quota를 확인하고 충전하세요.

---

## 레퍼런스

- [Hugo 문서](https://gohugo.io/documentation/)
- [Notion API 문서](https://developers.notion.com/)
- [OpenAI API 문서](https://platform.openai.com/docs)
- [GitHub Actions 문서](https://docs.github.com/en/actions)

---

**버전**: 1.0.0
**작성일**: 2026-02-04
**작성자**: OpenClaw Team
