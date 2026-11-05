#!/bin/bash
# 서비스에 배포한 양자화 모델을 팀 저장소(racheliee/kisia-project)의 고정 커밋에서 내려받습니다.
# 사용법: deploy 폴더에서 `bash download_models.sh`
set -euo pipefail

COMMIT=4e488ea5ec4d87ac757db4e04c8b5938d523f5b8
BASE="https://raw.githubusercontent.com/racheliee/kisia-project/${COMMIT}/models"
cd "$(dirname "$0")"

fetch() {
  mkdir -p "$(dirname "$2")"
  echo "download $2"
  curl -fsSL "${BASE}/$1" -o "$2"
}

fetch url_model/model-q.onnx                    url_model/model-q.onnx
fetch url_model/tokenizer/vocab.txt              url_model/tokenizer/vocab.txt
fetch url_model/tokenizer/tokenizer_config.json  url_model/tokenizer/tokenizer_config.json
fetch url_model/tokenizer/special_tokens_map.json url_model/tokenizer/special_tokens_map.json
fetch static_model/model50-q.bin                 static_model/model50-q.bin

sha256sum -c <<'EOF'
2a87e29f362ce4fea4d99acfd1a9ef6aadb47d47a2788db078f4c92afe8676cb  url_model/model-q.onnx
9dcfe8d02b1bedc71385338d436329a2d4ae9e61564a2b0d9940557a0b249372  static_model/model50-q.bin
EOF
