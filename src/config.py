"""
Configuration Module
환경 변수 로드, 경로 설정, 상수 정의를 담당합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 1. 경로 설정
# 현재 파일 위치: modules/intelligence/config.py
# 프로젝트 루트: OpenClaw/
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent  # modules/intelligence/../../ (즉, OpenClaw/)

# 주요 디렉토리
LOG_DIR = PROJECT_ROOT / "logs"
DATA_DIR = PROJECT_ROOT / "data"
ARCHIVE_DIR = PROJECT_ROOT / "archive"

# 디렉토리 생성
LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# 블로그 저장소 경로
BLOG_REPO_PATH_ENV = os.getenv("BLOG_REPO_PATH")
if BLOG_REPO_PATH_ENV:
    BLOG_REPO_PATH = Path(BLOG_REPO_PATH_ENV)
else:
    BLOG_REPO_PATH = PROJECT_ROOT / "security-blog"

# 블로그 URL
BLOG_URL = os.getenv("BLOG_URL", "https://rebugui.github.io/hate-coding-turtle/")

# 2. 환경 변수 로드
# 프로젝트 루트의 .env 파일 우선적으로 로드
env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    load_dotenv(env_path, override=True)
else:
    # 현재 디렉토리의 .env 시도
    local_env = PROJECT_ROOT / ".env"
    if local_env.exists():
        load_dotenv(local_env, override=True)

# 3. 설정 값 가져오기
def get_env(key: str, default: str = None) -> str:
    """환경 변수 가져오기"""
    return os.getenv(key, default)

# API Keys
OPENAI_API_KEY = get_env("OPENAI_API_KEY")
GLM_API_KEY = get_env("GLM_API_KEY")
NOTION_API_KEY = get_env("NOTION_API_KEY")

# Blog Config
BLOG_REPO_PATH = Path(get_env("BLOG_REPO_PATH", str(BLOG_REPO_PATH)))
BLOG_URL = get_env("BLOG_URL", "https://rebugui.github.io/hate-coding-turtle/")

# Database Config (Intelligence Agent)
DB_PATH = DATA_DIR / "intelligence.db"

# Notion Database ID (Intelligence Agent)
NOTION_DATABASE_ID = get_env("NOTION_DATABASE_ID") or get_env("BLOG_DATABASE_ID")

# Builder Agent Database ID
PROJECT_DATABASE_ID = get_env("PROJECT_DATABASE_ID") or get_env("BLOG_DATABASE_ID")

# LLM Config
GLM_BASE_URL = get_env("GLM_BASE_URL", "https://api.z.ai/api/coding/paas/v4/")
GLM_MODEL = get_env("GLM_MODEL", "glm-4.7")
