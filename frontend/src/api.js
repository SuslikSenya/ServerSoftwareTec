import axios from 'axios';

const API_URL = 'http://localhost:8000';

const getToken = () => localStorage.getItem('token');

const authHeaders = () => ({
    Authorization: `Bearer ${getToken()}`,
    'Content-Type': 'application/json',
});

// User by ID
export const fetchUserByName = async (userName) => {
    const response = await fetch(`${API_URL}/user/get_user_by_name/${userName}`, {
        headers: authHeaders(),
    });

    if (!response.ok) {
        throw new Error('Не удалось получить пользователя');
    }

    const userData = await response.json();

    const balance = userData.bills && userData.bills.length > 0
        ? userData.bills[0].amount_of_money
        : 0;

    return {
        ...userData,
        balance,
    };
};

// Create transaction
export const createTransaction = async (transactionData) => {
    const response = await fetch(`${API_URL}/user/create_transaction/`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify(transactionData),
    })

    if (!response.ok) {
        console.error("Error response:", await response.text());
        throw new Error('Failed to create transaction');
    }

    return await response.json()
}

// Get records
export const fetchRecords = async () => {
    // params = {}
    // const url = new URL(`${API_URL}/record`);
    const response = await fetch(`${API_URL}/record`, {
        method: 'GET',
        headers: authHeaders(),
    })

    // Object.keys(params).forEach(key => {
    //     if (params[key] !== undefined && params[key] !== null) {
    //         url.searchParams.append(key, params[key]);
    //     }
    // });


    if (!response.ok) {
        const errorText = await response.text();
        console.error('Ошибка при получении записи:', errorText);
        throw new Error('Не удалось получить записи');
    }

    return await response.json();
};

// Delete Record
export const deleteRecord = async (record_id) => { 
    try {
        const response = await fetch(`${API_URL}/record/${record_id}`, {
            method: 'DELETE',
            headers: authHeaders(),
        });
        return response.json();
    } catch (error) {
        alert('Ошибка при удалении записи');
        console.error(error);
    }
}


// Create Record
export const createRecord = async (newRecord) => {
    console.log(JSON.stringify(newRecord))
    const response = await fetch(`${API_URL}/record`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify(newRecord),
    })


    // const responseBody = await response.text();
    // console.log(responseBody)

    if (!response.ok) {
        const errorText = await response.text();
        console.error('Ошибка при создании записи:', errorText);
        throw new Error('Не удалось получить записи');
    }
    return await response.json()
}



// Create Category
export const createCategory = async (categoryData) => {
    const response = await fetch(`${API_URL}/category`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify(categoryData),
    });

    if (!response.ok) {
        throw new Error('Не удалось создать категорию');
    }

    return await response.json();
};


//Register User
export const registerUser = async (name, password) => {
    try {
        const response = await axios.post(`${API_URL}/user/register/`, { name, password });
        return response.data;
    } catch (error) {
        console.error('Registration failed', error);
        throw error;
    }
};