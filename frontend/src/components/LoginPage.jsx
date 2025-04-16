import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://127.0.0.1:8000/user/login', {
                username,
                password
            }, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            });

            localStorage.setItem('token', response.data.access_token); 
            navigate('/home');
        } catch (error) {
            setError('Неверные данные для входа');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white px-4">
            <div className="bg-gray-800 p-10 rounded-2xl shadow-xl text-center w-full max-w-md">
                <h1 className="text-3xl font-bold mb-6">Вход в систему</h1>
                <p className="mb-8 text-gray-300">Пожалуйста, введите свои данные для входа.</p>
                {error && <p className="text-red-500 mb-4">{error}</p>}
                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <label htmlFor="username" className="block text-sm font-semibold text-gray-300 mb-2">Логин</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-indigo-600"
                        />
                    </div>
                    <div>
                        <label htmlFor="password" className="block text-sm font-semibold text-gray-300 mb-2">Пароль</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-indigo-600"
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-indigo-600 hover:bg-indigo-700 transition px-6 py-2 rounded-lg font-semibold"
                    >
                        Войти
                    </button>
                </form>
                <div className="mt-6 text-sm text-gray-400">
                    <span>Нет аккаунта?</span>
                    <button
                        onClick={() => navigate('/register')}
                        className="ml-1 text-indigo-400 hover:text-indigo-600"
                    >
                        Зарегистрируйтесь
                    </button>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
