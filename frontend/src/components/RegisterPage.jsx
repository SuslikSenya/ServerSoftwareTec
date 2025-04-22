import React, { useState } from 'react';
import { registerUser } from '../api';
import { useNavigate } from 'react-router-dom';

const RegisterPage = () => {
    const [name, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            await registerUser(name, password);
            navigate('/home');
        } catch (error) {
            setError('Ошибка регистрации');
        }
    };


    // const handleRegister = async (e) => {
    //     e.preventDefault();
    // 
    //     try {
    //         const response = await axios.post('http://127.0.0.1:8000/user/register/', {
    //             username,
    //             password
    //         }, {
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             }
    //         });

    //         localStorage.setItem('token', response.data.access_token); // OAuth2 возвращает access_token
    //         navigate('/home');
    //     } catch (error) {
    //         setError('Неверные данные для входа');
    //     }
    // };





    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white px-4">
            <div className="bg-gray-800 p-10 rounded-2xl shadow-xl text-center w-full max-w-md">
                <h1 className="text-3xl font-bold mb-6">Регистрация</h1>
                {error && <p className="text-red-500 mb-4">{error}</p>}
                <form onSubmit={handleRegister} className="space-y-6">
                    <div>
                        <label htmlFor="name" className="block text-sm font-semibold text-gray-300 mb-2">Логин</label>
                        <input
                            type="text"
                            id="name"
                            value={name}
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
                        Зарегистрироваться
                    </button>
                </form>
                <div className="mt-6 text-sm text-gray-400">
                    <span>Уже есть аккаунт?</span>
                    <button
                        onClick={() => navigate('/login')}
                        className="ml-1 text-indigo-400 hover:text-indigo-600"
                    >
                        Войдите
                    </button>
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;
