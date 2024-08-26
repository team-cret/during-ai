# 베이스 이미지 설정
FROM ubuntu:20.04

# 필요한 패키지 업데이트 및 설치
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# `pip` 설치
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

# 파이썬 버전 확인
RUN python3.12 --version

# 작업 디렉토리 설정
WORKDIR /usr/src/during-ai

# requirements.txt 파일 복사
COPY requirements.txt ./

# Python 패키지 설치
RUN python3.12 -m pip install --upgrade pip \
    && python3.12 -m pip install -r requirements.txt

# 애플리케이션 파일 복사
COPY . .
