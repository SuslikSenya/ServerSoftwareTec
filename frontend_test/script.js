const apiUrl = "http://127.0.0.1:8000";

// Ссылки на элементы UI
const registerButton = document.getElementById('register-btn');
const loginButton = document.getElementById('login-btn');
const logoutButton = document.getElementById('logout-btn');
const createCategoryButton = document.getElementById('create-category-btn');
const createRecordButton = document.getElementById('create-record-btn');

const usernameRegister = document.getElementById('username-register');
const passwordRegister = document.getElementById('password-register');
const usernameLogin = document.getElementById('username-login');
const passwordLogin = document.getElementById('password-login');
const categoryName = document.getElementById('category-name');
const amountInput = document.getElementById('amount');

const registerMessage = document.getElementById('register-message');
const loginMessage = document.getElementById('login-message');
const userNameInfo = document.getElementById('user-name');
const userBalanceInfo = document.getElementById('user-balance');
const categoriesList = document.getElementById('categories-list');
const recordsList = document.getElementById('records-list');

// Регистрация пользователя
registerButton.onclick = async () => {
    const response = await fetch(`${apiUrl}/user/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: usernameRegister.value,
            password: passwordRegister.value,
        }),
    });

    const data = await response.json();
    if (response.status === 201) {
        registerMessage.textContent = "Регистрация прошла успешно!";
    } else {
        registerMessage.textContent = data.detail || "Ошибка при регистрации.";
    }
};

// Авторизация пользователя
loginButton.onclick = async () => {
    const response = await fetch(`${apiUrl}/user/login`, {
        method: 'POST',
        body: new URLSearchParams({
            username: usernameLogin.value,
            password: passwordLogin.value,
        }),
    });

    const data = await response.json();
    if (response.status === 200) {
        localStorage.setItem('token', data.access_token);
        fetchUserInfo();
    } else {
        loginMessage.textContent = data.detail || "Ошибка при авторизации.";
    }
};

// Логика выхода
logoutButton.onclick = () => {
    localStorage.removeItem('token');
    hideUserInfo();
};

// Получение информации о пользователе
async function fetchUserInfo() {
    const token = localStorage.getItem('token');
    if (!token) {
        return;
    }

    const response = await fetch(`${apiUrl}/user/${1}`, {  // замените 1 на реальный id пользователя
        headers: { 'Authorization': `Bearer ${token}` },
    });

    const data = await response.json();
    userNameInfo.textContent = `Имя: ${data.name}`;
    userBalanceInfo.textContent = `Баланс: ${data.user_bill}`;
    showUserInfo();
}

// Показать информацию о пользователе
function showUserInfo() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'none';
    document.getElementById('user-info').style.display = 'block';
    document.getElementById('categories-section').style.display = 'block';
    document.getElementById('records-section').style.display = 'block';
}

// Скрыть информацию о пользователе
function hideUserInfo() {
    document.getElementById('login-section').style.display = 'block';
    document.getElementById('register-section').style.display = 'block';
    document.getElementById('user-info').style.display = 'none';
    document.getElementById('categories-section').style.display = 'none';
    document.getElementById('records-section').style.display = 'none';
}

// Создание категории
createCategoryButton.onclick = async () => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${apiUrl}/category`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            name: categoryName.value,
        }),
    });

    const data = await response.json();
    if (response.status === 200) {
        const newCategory = document.createElement('li');
        newCategory.textContent = data.Category.name;
        categoriesList.appendChild(newCategory);
    }
};

// Создание записи
createRecordButton.onclick = async () => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${apiUrl}/record`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            user_id: 1,  // Замените на реальный ID
            category_id: 1,  // Замените на реальный ID категории
            amount: amountInput.value,
            date: new Date().toISOString(),
        }),
    });

    const data = await response.json();
    if (response.status === 200) {
        const newRecord = document.createElement('li');
        newRecord.textContent = `Сумма: ${data.Record.amount}`;
        recordsList.appendChild(newRecord);
    }
};
