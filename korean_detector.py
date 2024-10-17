import re
import asyncio


class KoreanDetector:
    korean_pattern = re.compile(r'[가-힣]')
    english_pattern = re.compile(r'[a-zA-Z]')
    unknown_pattern = re.compile(r'[^가-힣a-zA-Z]')

    korean_particles = {
        '이', '가', '을', '를', '에', '에서', '으로', '로', '와', '과', '하고', '의',
        '도', '만', '은', '는', '까지', '조차', '밖에', '다', '입니다', '요', '죠', '지요',
        '네요', '십시오', '고', '서', '며', '면서', '지만', '는데', 'ㄴ', '는', 'ㄹ', '을', '던',
        '그리고', '그러나', '그래서', '그러므로'
    }

    english_particles = {
        'in', 'on', 'at', 'by', 'with', 'about', 'for', 'from', 'to', 'of',
        'into', 'onto', 'up', 'down', 'across', 'over', 'under', 'through',
        'between', 'among', 'a', 'an', 'the', 'and', 'or', 'but', 'so', 'as',
        'if', 'when', 'than', 'because', 'am', 'are', 'is', 'was', 'were',
        'be', 'been', 'being'
    }

    def __init__(self, korean_message="ko", english_message="en", unknown_message=None):
        self.korean_message = korean_message
        self.english_message = english_message
        self.unknown_message = unknown_message

    async def detect_language(self, text):
        if isinstance(text, str):
            return await self._detect_single_language(text)
        elif isinstance(text, list):
            return await self._detect_multiple_languages(text)
        else:
            raise TypeError("Input must be a string or a list of strings.")

    async def _detect_single_language(self, text):
        if text.isdigit():
            return self.korean_message

        text_cleaned = re.sub(r'[\d\s\W_]+', '', text)

        korean_count = len(re.findall(self.korean_pattern, text_cleaned))
        english_count = len(re.findall(self.english_pattern, text_cleaned))

        total_count = korean_count + english_count
        if total_count == 0:
            return self.unknown_message

        korean_ratio = korean_count / total_count
        english_ratio = english_count / total_count

        contains_unknown = bool(re.findall(self.unknown_pattern, text_cleaned))

        contains_korean_particles = any(particle in text_cleaned for particle in self.korean_particles)
        contains_english_particles = any(particle in text_cleaned for particle in self.english_particles)

        if contains_unknown:
            if contains_korean_particles and korean_ratio >= english_ratio:
                return self.korean_message
            elif contains_english_particles and english_ratio > korean_ratio:
                return self.english_message
            else:
                return self.unknown_message
        elif english_ratio > 0.6 and not contains_korean_particles:
            return self.english_message
        elif english_ratio > 0.6 and contains_korean_particles and english_count > korean_count * 2:
            return self.english_message
        elif korean_ratio > 0.5 or contains_korean_particles:
            return self.korean_message
        else:
            return self.english_message if english_ratio >= korean_ratio else self.korean_message

    async def _detect_multiple_languages(self, texts):
        tasks = [self._detect_single_language(text) for text in texts]
        return await asyncio.gather(*tasks)
