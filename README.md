# 악성 URL·JavaScript 탐지 모델

웹사이트의 **URL**과 페이지가 불러오는 **JavaScript 코드**를 각각 분석해 악성 여부를 판정하는 두 모델, 그리고 이를 서비스 서버에 올리기 위해 INT8로 양자화한 배포 버전입니다.

> **제2회 KISIA 정보보호 개발자 해커톤 최우수상** (과학기술정보통신부 장관상, 2024.08)
>
> 2024 KISIA 해커톤과 AI보안 기술개발 교육(네트워크반)에서 4인 팀으로 만든 악성 URL 탐지 서비스의 AI 모델 부분입니다. 전체 서비스(크롬 확장 프로그램, 백엔드, 대시보드)는 [racheliee/kisia-project](https://github.com/racheliee/kisia-project)에 있습니다.

**맡은 일** (팀장, AI 모델 담당): URL 모델과 JS 정적 분석 모델 학습, 정상 JS 수집, 추론 API, 배포용 양자화, 탐지기 앙상블 구성 참여

## 왜 모델이 두 개인가

URL만 보는 모델은 처음 보는 URL에 약했습니다. 학습 데이터와 같은 출처에서는 F1 0.99였지만, 다른 출처의 URL 데이터셋에서는 F1 0.68로 떨어졌습니다. 재현율은 0.99로 유지됐지만 정밀도가 0.54여서, 정상 URL을 악성으로 판정하는 경우가 많았다는 뜻입니다.

| 평가 데이터 | 정밀도 | 재현율 | F1 |
| --- | --- | --- | --- |
| 학습과 같은 출처 ([malicious-urls-dataset](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset), 130,239개, 악성 클래스 기준) | 0.99 | 0.98 | 0.99 |
| 다른 출처 ([urldataset](https://www.kaggle.com/datasets/antonyj453/urldataset), 팀 최종 발표 기준) | 0.54 | 0.99 | 0.68 |

그래서 URL 문자열 대신 페이지가 실제로 실행하는 코드를 보는 정적 분석 모델을 함께 만들었습니다. 팀 서비스에서는 이 두 모델에 동적 분석(실행 행위)과 네트워크 패킷 탐지기를 더한 4개 탐지기의 결과를 정확도에 따라 가중치를 주어 합쳤습니다.

## 모델

### URL 분류기 (`url_model/`)

URL 문자열을 그대로 문장처럼 읽어 정상/악성을 분류합니다. 사전학습된 DistilBERT(`distilbert-base-uncased`)를 미세조정했습니다.

- 데이터: malicious-urls-dataset 651,191개를 학습·검증 520,952 / 평가 130,239로 나눔
- 학습: Colab A100, 혼합 정밀도, AdamW, lr 5e-5, early stopping
- 결과(같은 출처 평가): 정확도 0.991. 혼동 행렬과 학습 곡선은 [train/url/README.md](train/url/README.md)에 있습니다.

### JavaScript 정적 분석 분류기 (`static_model/`)

코드를 실행하지 않고 구조만 보고 판정합니다. 변수 이름이나 문자열은 난독화로 쉽게 바뀌지만, 코드가 어떤 문법 구조로 이루어졌는지는 덜 바뀌기 때문입니다.

1. Esprima로 코드를 구문 트리(AST)로 바꿉니다.
2. 트리를 깊이 우선으로 돌며 노드 종류만 한 줄로 늘어놓습니다.
3. 이 한 줄을 문장으로 보고 fastText로 분류합니다. 코드 길이가 수백에서 수만 토큰까지 제각각이라, 긴 입력도 빠르게 처리하는 fastText를 골랐습니다.

실제 변환 예시:

```text
var s = document.createElement("script");
s.src = "http://example.com/a.js";
document.body.appendChild(s);

→ Program VariableDeclaration VariableDeclarator Identifier
  CallExpression MemberExpression Identifier Identifier Literal
  ExpressionStatement AssignmentExpression MemberExpression Identifier Identifier Literal
  ExpressionStatement CallExpression MemberExpression MemberExpression
  Identifier Identifier Identifier Identifier
```

- 데이터: 악성 JS는 [javascript-malware-collection](https://github.com/HynekPetrak/javascript-malware-collection), 정상 JS는 네이버·구글·페이스북·인스타그램 등에서 직접 수집. 학습 악성 13,622 / 정상 17,270, 평가 1,000 / 1,000
- 결과: 정밀도 0.85, 재현율 0.91, F1 0.86

<img src="docs/images/static_eval_hist.png" width="520" alt="평가 스크립트 2,000개에 대한 악성 확률 분포">

평가 스크립트 2,000개에 대해 모델이 낸 악성 확률의 분포입니다. 정상 코드(파랑)는 0 근처에, 악성 코드(주황)는 1 근처에 몰려 있어 두 집단이 잘 갈립니다.

## 배포용 양자화 (`deploy/`)

서비스 서버에서 요청마다 바로 돌릴 수 있도록 두 모델을 양자화해 크기를 줄였습니다. URL 모델은 약 4배 작아지고 2.5배 빨라졌으며, 샘플 입력에서 원본과 판정이 모두 같았습니다.

| 모델 | 원본 → 배포본 | 크기 | 지연시간 |
| --- | --- | --- | --- |
| URL | PyTorch FP32 → ONNX INT8 | 268 → 67 MB | 29.7 → 11.8 ms |
| JavaScript | fastText 100차원 → 50차원 + 양자화 | 800 → 52 MB | 4.4 → 6.4 ms |

- URL 모델: 선형층 가중치를 8비트 정수로 저장하고, 선형층 입력도 추론할 때마다 8비트로 바꿔 정수 곱셈을 하는 동적 양자화를 적용했습니다.
- JavaScript 모델: 단어 벡터 차원을 50으로 줄여 다시 학습한 뒤, fastText의 양자화 기능으로 벡터를 압축했습니다.
- 측정 조건: 2026.11 재측정, 2코어 x86 CPU, `test_flask/`의 샘플 URL 8개·스크립트 8개를 하나씩 추론한 시간의 중앙값. JS는 AST 변환 시간을 포함합니다.
- JS 모델은 크기만 줄었고 속도 이득은 없었습니다. 추론 한 번에 AST 변환이 약 3.8 ms로 대부분을 차지하고, fastText 계산 자체는 양자화 후 0.6 → 1.7 ms로 오히려 늘었습니다. 압축된 벡터를 복원하는 비용 때문으로 보입니다.
- 배포본은 팀 서비스 백엔드가 실제로 사용한 파일과 같습니다(SHA-256 일치).

## 실행

Python 3.10–3.11을 권장합니다. fastText 파이썬 바인딩이 NumPy 2와 호환되지 않아 `numpy==1.23`을 씁니다. 원본 모델 가중치는 Git LFS로 관리하므로 [git-lfs](https://git-lfs.com)가 필요합니다.

**원본 모델 API**

```bash
git lfs install
git clone https://github.com/seungwooLee00/malicious-url-detection
cd malicious-url-detection
pip install -r requirements.txt
python -m test_flask.app            # http://127.0.0.1:5000

bash test_flask/requestURL.sh       # 다른 터미널에서: 샘플 URL 8개 판정
bash test_flask/requestJS.sh        # 샘플 스크립트 8개 판정
```

**양자화 모델 API**

```bash
cd deploy
bash download_models.sh             # 팀 저장소의 고정 커밋에서 배포 모델을 받고 해시 확인
pip install -r requirements.txt
python app.py                       # http://127.0.0.1:5000, 엔드포인트는 원본과 같음
```

엔드포인트는 `POST /predictURL`, `POST /predictJS` 두 개이고, `files[]` 필드로 파일 여러 개를 받아 각각의 결과를 돌려줍니다.

```json
[{"prediction": "benign", "confidence": 0.9753}, {"prediction": "malicious", "confidence": 0.9998}]
```

## 구조

```text
url_model/      URL 분류기 (DistilBERT, 가중치는 Git LFS)
static_model/   JS 정적 분석 분류기 (fastText, 가중치는 Git LFS)
train/          학습 코드와 노트북 (url/, static/)
test_flask/     원본 모델 추론 API와 샘플 요청 스크립트
test/           오프라인 추론 시간 측정 스크립트 (데이터 미포함)
deploy/         서비스 배포용 양자화 모델 API
```

## 한계

- URL 모델은 학습 데이터의 URL 형식에 과적합되어 있습니다. 샘플 URL로 다시 확인하면 앞에 `https://`가 붙었는지에 따라 판정이 바뀝니다. 그래서 서비스에서는 단독으로 쓰지 않고 다른 탐지기와 함께 썼습니다.
