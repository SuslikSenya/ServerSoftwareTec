import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchUserByName, createTransaction, fetchRecords, createRecord, deleteRecord } from '../api';
import { Spin } from 'antd';
import { jwtDecode } from 'jwt-decode';

const HomePage = () => {
    const [user, setUser] = useState(null);
    const [transactionData, setTransactionData] = useState({
        user_name: '',
        amount: '',
        description: '',
        timestamp: new Date().toISOString(),
    });
    
    const [records, setRecords] = useState([]);
    const [recordsFetched, setRecordsFetched] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newRecord, setNewRecord] = useState({
        user_id: user?.id || '',
        category_id: '',
        date: new Date().toISOString(),
        amount: '',
    });

    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setTransactionData({
            ...transactionData,
            [name]: value
        });
    };

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
        } else {
            const decodedToken = jwtDecode(token);
            console.log(decodedToken);
            const userName = decodedToken.sub;
            console.log(userName);
            fetchUserData(userName);
            // fetchRecordsData(); // Загружаем записи
        }
    }, [navigate]);

    const fetchUserData = async (userName) => {
        try {
            const data = await fetchUserByName(userName);
            setUser(data);
            setNewRecord((prev) => ({
                ...prev,
                user_id: data.id,
            }));
            setLoading(false);
        } catch (error) {
            alert('Error while loading user data');
            console.error(error);
            navigate('/login')
        }
    };

    const handleLogout = () => { 
        localStorage.removeItem('token')
        navigate('/login')
    }

    // GET Record
    const fetchRecordsData = async () => {
        try {
            const response = await fetchRecords({  });
            setRecords(response.data);
            setRecordsFetched(true);
        } catch (error) {
            alert('Error while loading records');
            console.error(error);
        }
    };

    // Delete Record
    const handleDeleteRecord = async (record_id) => {
        console.log(record_id)
        const confirmed = window.confirm('Вы уверены, что хотите удалить эту запись?');
        if (confirmed) {
            const response = await deleteRecord(record_id);
            if (response) {
                setRecords((prevRecords) => prevRecords.filter(record => record.id !== record_id));
            }
        }
    };

    // Create Record
    const handleRecordInputChange = (e) => {
        const { name, value } = e.target;
        setNewRecord((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleCreateRecord = async () => {
        try {
            const recordToSend = {
                ...newRecord,
                category_id: parseInt(newRecord.category_id, 10),
                amount: parseInt(newRecord.amount, 10),
                date: new Date(newRecord.date).toISOString().slice(0, 19),
            };
            console.log(recordToSend.date)
            await createRecord(recordToSend);
            const response = await fetchRecords();
            setRecords(response.data);
            setIsModalOpen(false);
            fetchRecordsData();
        } catch (error) {
            alert('Error while creating records');
            console.error(error); // Выведи ошибку в консоль для диагностики
        }
    };

    

    const handleCreateTransaction = async () => {
        try {
            await createTransaction(transactionData);
            // fetchUserData(); // Обновляем данные пользователя после транзакции
            setTransactionData({
                user_name: '',
                description: '',
                amount: '',
                timestamp: new Date().toISOString(),
            })
        } catch (error) {
            alert('Error during transaction creation');
            console.error(error); // Выведи ошибку в консоль для диагностики
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center min-h-screen bg-gray-900 text-white">
                <Spin size="large" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-900 text-white px-4">
            <div className="bg-gray-800 p-10 rounded-2xl shadow-xl text-center w-full max-w-md mx-auto my-6">
                <div className="flex justify-end mb-4">
                    <button
                        onClick={handleLogout}
                        className="bg-red-600 hover:bg-red-700 transition px-4 py-2 rounded-lg font-semibold"
                    >
                        Выйти
                    </button>
                </div>
                <h1 className="text-3xl font-bold mb-4">Добро пожаловать, {user.name}</h1>
                <h2 className="text-xl mb-6">Ваш баланс: {user.user_bill}</h2>

                {/* Форма для транзакции */}
                <div className="mb-8">
                    <h2 className="text-2xl font-semibold mb-4">Создать транзакцию</h2>
                    <form onSubmit={(e) => e.preventDefault()} className="space-y-4">
                        <div>
                            <label htmlFor="user_name" className="block text-sm font-semibold text-gray-300">Получатель:</label>
                            <input
                                type="text"
                                name="user_name"
                                value={transactionData.user_name}
                                onChange={handleInputChange}
                                placeholder="Введите имя получателя"
                                className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-indigo-600"
                            />
                        </div>

                        <div>
                            <label htmlFor="description" className="block text-sm font-semibold text-gray-300">Описание:</label>
                            <input
                                type="text"
                                name="description"
                                value={transactionData.description}
                                onChange={handleInputChange}
                                placeholder="Введите описание транзакции"
                                className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-indigo-600"
                            />
                        </div>

                        <div>
                            <label htmlFor="amount" className="block text-sm font-semibold text-gray-300">Сумма:</label>
                            <input
                                type="number"
                                name="amount"
                                value={transactionData.amount}
                                onChange={handleInputChange}
                                placeholder="Введите сумму"
                                className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-indigo-600"
                            />
                        </div>

                        <button
                            type="button"
                            onClick={handleCreateTransaction}
                            className="w-full bg-indigo-600 hover:bg-indigo-700 transition px-6 py-2 rounded-lg font-semibold"
                        >
                            Отправить деньги
                        </button>
                    </form>
                </div>

                {/* Отображение записей */}
                <div>
                    <h2 className="text-2xl font-semibold mb-4">Мои записи</h2>
                    <div className="flex justify-between mb-4">
                        <button
                            onClick={fetchRecordsData}
                            className="bg-indigo-600 hover:bg-indigo-700 transition px-6 py-2 rounded-lg font-semibold"
                        >
                            Показать записи
                        </button>
                        <button
                            onClick={() => setIsModalOpen(true)}
                            className="bg-gray-700 hover:bg-gray-600 transition px-6 py-2 rounded-lg font-semibold"
                        >
                            Создать запись
                        </button>
                    </div>

                    {records.length > 0 ? (
                        records.map((record) => (
                            <div key={record.id} className="bg-gray-700 p-4 rounded-lg mb-4">
                                <h3 className="text-xl font-semibold">{record.title}</h3>
                                <p className="text-gray-300"><strong>Описание:</strong> Запись №{record.id}</p>
                                <p className="text-gray-300"><strong>Дата создания:</strong> {new Date(record.date).toLocaleDateString()}</p>

                                <div className="flex justify-between mt-4">
                                    <button className="bg-indigo-600 hover:bg-indigo-700 transition px-4 py-2 rounded-lg font-semibold">Редактировать</button>
                                    <button
                                        onClick={() => handleDeleteRecord(record.id)}
                                        className="bg-red-600 hover:bg-red-700 transition px-4 py-2 rounded-lg font-semibold">Удалить
                                    </button>
                                </div>
                            </div>
                        ))
                    ) : recordsFetched ? (
                        <div className="text-center text-gray-400">У вас пока нет записей</div>
                    ) : (
                        <div className="text-center text-gray-400">Нажмите "Показать Записи" чтобы посмотреть свои записи</div>
                    )}
                </div>
            </div>
            {isModalOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
                    <div className="bg-gray-800 p-6 rounded-xl w-full max-w-md">
                        <h2 className="text-xl font-bold mb-4 text-white">Создание записи</h2>

                        <input
                            type="number"
                            name="category_id"
                            placeholder="Category ID"
                            value={newRecord.category_id}
                            onChange={handleRecordInputChange}
                            className="mb-2 w-full p-2 rounded bg-gray-700 text-white"
                        />

                        <input
                            type="datetime-local"
                            name="date"
                            value={newRecord.date.slice(0, 16)}
                            onChange={handleRecordInputChange}
                            className="mb-2 w-full p-2 rounded bg-gray-700 text-white"
                        />

                        <input
                            type="number"
                            name="amount"
                            placeholder="Amount"
                            value={newRecord.amount}
                            onChange={handleRecordInputChange}
                            className="mb-4 w-full p-2 rounded bg-gray-700 text-white"
                        />

                        <div className="flex justify-between">
                            <button
                                onClick={handleCreateRecord}
                                className="bg-indigo-600 px-4 py-2 rounded text-white font-semibold"
                            >
                                Создать
                            </button>
                            <button
                                onClick={() => setIsModalOpen(false)}
                                className="bg-red-600 px-4 py-2 rounded text-white font-semibold"
                            >
                                Отмена
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default HomePage;
