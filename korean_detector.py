import re
import asyncio
from korean_keywords import korean_keywords
from english_keywords import english_keywords

class KoreanDetector:
    korean_pattern = re.compile(r'[가-힣]')
    english_pattern = re.compile(r'[a-zA-Z]')
    mention_pattern = re.compile(r'<@!?[0-9]+>')

    korean_particles = {
        '이', '가', '을', '를', '에', '에서', '으로', '로', '와', '과', '하고', '의',
        '도', '만', '은', '는', '까지', '조차', '밖에', '다', '입니다', '요', '죠', '지요',
        '네요', '십시오', '고', '서', '며', '면서', '지만', '는데', 'ㄴ', '는', 'ㄹ', '을', '던',
        '그리고', '그러나', '그래서', '그러므로', '했어요', '어'
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
        text_cleaned = re.sub(r'[^\w]', '', text)

        if text_cleaned.isdigit():
            return self.korean_message

        text_without_numbers = re.sub(r'\d+', '', text_cleaned)

        korean_count = len(re.findall(self.korean_pattern, text_without_numbers))
        english_count = len(re.findall(self.english_pattern, text_without_numbers))

        total_count = korean_count + english_count
        if total_count == 0:
            return self.unknown_message

        korean_ratio = korean_count / total_count
        english_ratio = english_count / total_count

        if english_ratio >= 0.8:
            return self.english_message
        elif korean_ratio >= 0.8:
            return self.korean_message

        korean_weight = self._calculate_weight(text_without_numbers, self.korean_particles, korean_keywords, ratio=korean_ratio)
        english_weight = self._calculate_weight(text_without_numbers, self.english_particles, english_keywords, ratio=english_ratio)

        korean_weight += self._check_end_of_sentence(text_without_numbers, self.korean_pattern)
        english_weight += self._check_end_of_sentence(text_without_numbers, self.english_pattern)

        if korean_weight > english_weight:
            return self.korean_message
        elif english_weight > korean_weight:
            return self.english_message

        return self.unknown_message

    def _calculate_weight(self, text, particles, keywords, ratio):
        weight = ratio
        for particle in particles:
            if particle in text:
                weight += 1.5
        for keyword in keywords:
            if keyword in text:
                weight += 0.5
        return weight

    def _check_end_of_sentence(self, text, pattern):
        end_check = re.search(pattern, text[-1:])
        return 2.0 if end_check else 0.0

    async def _detect_multiple_languages(self, texts):
        tasks = [self._detect_single_language(text) for text in texts]
        return await asyncio.gather(*tasks)
