import asyncio
from korean_detector import KoreanDetector

detector = KoreanDetector(korean_message="ko", english_message="en", unknown_message=None) # 반환 값 설정 가능

async def process_single_text():
    text = "Hello"
    result = await detector.detect_language(text)
    print(result)  # en

async def process_multiple_texts():
    texts = ["Hello", "안녕하세요", "12345"]
    results = await detector.detect_language(texts)
    print(results)  # ['en', 'ko', 'ko']

async def unknown_text():
    text = "テスト"
    result = await detector.detect_language(text)
    print(result) # None

asyncio.run(process_single_text())
asyncio.run(process_multiple_texts())
asyncio.run(unknown_text())
