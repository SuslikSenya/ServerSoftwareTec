# Backend-Tech
## Labs for Backend Technologies

### Instructions on How to Run the Program Locally

1. **Install Docker Desktop** on your computer.
2. **Clone the repository** to your local machine.
3. Open your terminal and navigate to the directory containing your `docker-compose.yml` file.
4. Run the following command to build and start your application:
   ```bash
   docker-compose up --build
5. Once the application starts, open your web browser and go to http://localhost:8000/docs.


### Варіант завдання для третьої лабораторної роботи


Варіант визначаємо за остачею від ділення свого номеру групи на 3.
Мій варіант = 2424, звідси **2424 % 3 = 0**.
- Отже, моє завдання - Облік доходів

Облік доходів - потрібно зробити сутність “рахунок” куди можна додавати гроші по мірі їх надходження
(для кожного користувача свій) і звідти списуються кошти атоматично при створенні нової витрати. 
Логіка щодо заходу в мінус лишається на розсуд студентів(можете або дозволити це, або заборонити).

#### Для виконання цього завдання я зробив:
- Файл зі схемами та моделями для бд, та зручності використання.
- Перевів увесь код у асинхронний формат.
- Підключив базу данних для мого застосунку.
- Зробив логіку обробки транзакцій і обілку доходів.