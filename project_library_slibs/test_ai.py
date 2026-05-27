from mistral_client import get_ai_answer

# 1. Первый запрос (истории нет)
print("Запрос 1:")
ans1, hist = get_ai_answer("Назови трех французских художников.")
print(ans1)

# 2. Второй запрос (передаем историю hist)
print("\nЗапрос 2 (с памятью):")
ans2, hist2 = get_ai_answer("А назови трех русских.", history=hist)
print(ans2)