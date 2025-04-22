import React from 'react';
import { useNavigate } from 'react-router-dom';


const WelcomePage = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white px-4">
            <div className="bg-gray-800 p-10 rounded-2xl shadow-xl text-center w-full max-w-md">
                <h1 className="text-3xl font-bold mb-6">Добро пожаловать на сайт!</h1>
                <p className="mb-8 text-gray-300">Пожалуйста, войдите или зарегистрируйтесь, чтобы продолжить.</p>
                <div className="flex justify-center gap-4">
                    <button
                        onClick={() => navigate('/login')}
                        className="bg-indigo-600 hover:bg-indigo-700 transition px-6 py-2 rounded-lg font-semibold"
                    >
                        Войти
                    </button>
                    <button
                        onClick={() => navigate('/register')}
                        className="bg-gray-700 hover:bg-gray-600 transition px-6 py-2 rounded-lg font-semibold"
                    >
                        Регистрация
                    </button>
                </div>
            </div>
        </div>
    );
};

export default WelcomePage;
