## ❤️ Скрипт для отправки комплиментов любимой девушке по рассписанию

1. Зарегистрируйте Open AI API ключ: https://platform.openai.com/account/api-keys
2. Зарегистрируйте приложение для Telegram: https://my.telegram.org/
3. Склонируйте этот репозиторий и зайдите в папку с файлами репозитория
4. Создайте .env файл на основе примера .env.example со своими значениями
5. Дня начала соберите приложение:  
``
docker build -t send_compliment .
``
6. Потом вызовите функцию:  
``
docker run --rm -it send_compliment
``
