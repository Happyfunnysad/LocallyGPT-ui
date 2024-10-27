import g4f

class GptClient:
    def __init__(self):
        # Получаем список доступных моделей из g4f
        self.models = self._get_available_models()

    def _get_available_models(self):
        # Здесь вы можете получить список моделей, поддерживаемых g4f
        # Если g4f не предоставляет метод для этого, определите список вручную
        return [
            #'o1',
            'gpt-4o',
            'gpt-4o-mini',
            'sonar-chat', 
            #'grok-2', #low limit
            'grok-2-mini',
            'gemini-pro',
            'claude-3.5-sonnet',
            'claude-3-opus',
            'nemotron-70b',
            'mixtral-8x22b',
            'meta-ai',
            'hermes-3',
            
            

        ]

    def get_models(self):
        return self.models

    def send_message(self, model_name, messages):
        try:
            response = g4f.ChatCompletion.create(
                model=model_name,
                messages=messages,
                stream=False  # Можно установить True для потокового вывода
            )
            return response
        except Exception as e:
            # Возвращаем строку ошибки, чтобы она могла быть отображена в интерфейсе
            return f"Ошибка: {e}"