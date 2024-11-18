# TextSituationParser
상황 분류 모델입니다

### 제미나이 사용을 하기위해 설치해주셔야합니다.

```bash
pip install google-generativeai
```

### 안쪽에 API 키를 입력하는 란이있습니다.
```python

from test import TextSituationParser

GOOGLE_API_KEY = 'your_API_key'
input_text = (
        '일기 텍스트 넣기'
    )

parser = TextSituationParser(api_key=GOOGLE_API_KEY)
answer_dict = parser(input_text)
print("결과 :", answer_dict)

```
