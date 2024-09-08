import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
    const [searchValue, setSearchValue] = useState("")
    const navigate = useNavigate()

    const handleSubmit = (e) => {
        e.preventDefault()
        if (searchValue === "logout") {
            localStorage.clear()
            navigate("/login")
        } else {
            navigate(`/chat/${searchValue}`) 
        }
    }

    return (
        <div id="search-bar" className="w-120 bg-white rounded-md shadow-lg z-10" onSubmit={handleSubmit}>
        <form className="flex items-center justify-center min-h-screen">
            <input
            type="text"
            placeholder="Enter your channel/Enter logout to sign out"
            className="w-96 rounded-md px-2 py-1 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:border-transparent"
            value={searchValue}
            required
            onChange={(e) => setSearchValue(e.target.value)}
            />
            <button
            type="submit"
            className="bg-gray-800 text-white rounded-md px-4 py-1 ml-2 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:ring-opacity-50"
            >
            Search
            </button>
        </form>
        </div>
    );
};

export default Home;
