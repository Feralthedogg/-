`KoreanDetector`는 텍스트에서 한국어와 영어를 감지하고, 알 수 없는 문자가 포함된 경우 `None`을 반환하는 비동기 파이썬 라이브러리입니다. 이 라이브러리는 한국어 조사 및 영어 전치사를 기반으로 텍스트의 언어를 판별하며, 문장의 끝부분이 해당 언어로 끝나는 경우 가중치를 부여하여 보다 정확한 판별을 제공합니다. 비동기 처리(`asyncio`)를 사용하여 대량의 텍스트를 효율적으로 처리할 수 있습니다.

## 주요 기능

- **한국어/영어 감지**: 주어진 텍스트에서 한국어와 영어 비율을 계산하여 주 언어를 판별합니다.
- **문장 끝 가중치**: 문장의 끝부분이 한국어 혹은 영어로 끝나는 경우 추가 가중치를 부여합니다.
- **알 수 없는 문자 처리**: 한국어 및 영어에 속하지 않는 문자가 포함된 경우 `None`을 반환합니다.
- **비동기 처리**: 여러 개의 텍스트를 비동기적으로 병렬 처리할 수 있습니다.
- **리스트와 문자열 모두 지원**: 단일 문자열(`str`)과 여러 텍스트(`list`) 입력을 모두 지원합니다.

## 설치 방법

`KoreanDetector`는 파이썬 3.x 환경에서 동작합니다. 설치할 필요 없이 `korean_detector.py` 파일을 프로젝트에 추가한 후 사용하세요.

## 사용법

### 단일 문자열 처리

단일 문자열에서 한국어 또는 영어를 감지하는 예제입니다.

```python
import asyncio
from korean_detector import KoreanDetector

detector = KoreanDetector(korean_message="ko", english_message="en", unknown_message=None)

async def process_single_text():
    text = "Hello"
    result = await detector.detect_language(text)
    print(result)  # 'en'

asyncio.run(process_single_text())
```

### 여러 텍스트 처리

여러 텍스트를 리스트로 입력하여 비동기적으로 처리할 수 있습니다.

```python
import asyncio
from korean_detector import KoreanDetector

detector = KoreanDetector(korean_message="ko", english_message="en", unknown_message=None)

async def process_multiple_texts():
    texts = ["Hello", "안녕하세요", "12345"]
    results = await detector.detect_language(texts)
    print(results)  # ['en', 'ko', 'ko']

asyncio.run(process_multiple_texts())
```

### 옵션 설정

- `korean_message`: 한국어로 판정된 경우 반환할 메시지 (기본값: `"ko"`)
- `english_message`: 영어로 판정된 경우 반환할 메시지 (기본값: `"en"`)
- `unknown_message`: 알 수 없는 문자가 포함된 경우 반환할 메시지 (기본값: `None`)

```python
detector = KoreanDetector(korean_message="한국어", english_message="영어", unknown_message="알 수 없음")
```

### 비동기 처리

비동기 처리를 사용하여 대규모 데이터 처리 성능을 개선할 수 있습니다.

```python
async def process_large_dataset():
    texts = ["Text 1", "Text 2", ...]  # 수많은 텍스트 입력
    results = await detector.detect_language(texts)
    print(results)

asyncio.run(process_large_dataset())
```

## 내부 동작

1. **정규식 기반 언어 감지**: `re` 모듈을 사용하여 텍스트에서 한국어(`가-힣`)와 영어(`a-zA-Z`) 문자를 감지합니다.
2. **조사 및 전치사 기반 판별**: 한국어의 조사와 영어의 전치사를 기반으로 문장의 언어를 판별합니다.
3. **문장 끝 가중치 부여**: 문장의 끝이 한국어 또는 영어로 끝나는 경우, 해당 언어에 추가 가중치를 부여하여 정확도를 높입니다.
4. **언어 비율 계산 및 임계값 설정**: 텍스트 내에서 한국어와 영어 비율을 계산하고, 일정 비율 이상이면 그 언어로 판정합니다.
5. **비동기 처리**: `asyncio`를 통해 대규모 데이터를 효율적으로 처리할 수 있습니다.

## 성능 최적화

- **정규식 미리 컴파일**: `re.compile`을 사용하여 정규식을 미리 컴파일하여 성능을 최적화했습니다.
- **Set 자료형을 사용한 빠른 검색**: 한국어와 영어의 조사 및 전치사를 리스트 대신 `set` 자료형으로 관리하여 빠른 검색 성능을 제공합니다.
- **비동기 처리 지원**: `asyncio.gather`를 사용하여 여러 텍스트를 동시에 처리하여 성능을 향상시킵니다.

## 예외 처리

- **입력 타입 오류**: 입력 데이터가 문자열 또는 리스트가 아닐 경우 `TypeError`가 발생합니다.
- **비동기 처리 오류**: 비동기 함수가 적절하게 사용되지 않을 경우 `asyncio.run`을 통해 실행해야 합니다.

```python
try:
    await detector.detect_language(123)
except TypeError as e:
    print(e)  # "Input must be a string or a list of strings."
```
GPT 작성
