# example.py
import asyncio
from korean_detector import KoreanDetector

detector = KoreanDetector(korean_message="한국어", english_message="영어", unknown_message=None)  # 반환 값 설정 가능

async def process_single_text(detector):
    text = "Hello"
    result = await detector.detect_language(text)
    print(result) # 영어

async def idk(detector):
    text = "san francisco에 가서 meat ball 스파게티를 eat하고 korea로 복귀했어요"
    result = await detector.detect_language(text)
    print(result) # 한국어

async def process_multiple_texts(detector):
    texts = ["Hello", "안녕하세요", "12345"]
    results = await detector.detect_language(texts)
    print(results) # ['영어', '한국어', '한국어']

async def unknown_text(detector):
    text = "テスト"
    result = await detector.detect_language(text)
    print(result) # None

async def choseung_text(detector):
    text = "bbㅋㅋㅋㅋㅋㅋ"
    result = await detector.detect_language(text)
    print(result) # 한국어

async def main():
    await process_single_text(detector)
    await idk(detector)
    await process_multiple_texts(detector)
    await unknown_text(detector)
    await choseung_text(detector)

if __name__ == "__main__":
    asyncio.run(main())
