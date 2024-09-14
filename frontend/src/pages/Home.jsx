import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Home = () => {
    const [roomName, setRoomName] = useState("")
    const [roomPassWord, setRoomPassWord] = useState("")
    const localUser = localStorage.getItem("username")
    const navigate = useNavigate()

    const handleSubmit = (e) => {
        e.preventDefault()
        if (searchValue === "logout") {
            localStorage.clear()
            navigate("/login")
        } else {
            navigate(`/chat/${roomName}`) 
        }
    }

    const handleCreateRoom = async (e) => {
        try {
            const res = await api.post("/api/create/chatroom/", {
                'room_name': roomName,
                'password': roomPassWord,
                'usernames': [localUser]
            })
            if (res.status === 201) {
                navigate(`/chat/${roomName}`)
            }
        } catch (error) {
            console.log(error)
        }
    }

    const handleKeyUp = (e) => {
        if (e.keyCode === 13) {
            handleSubmit()
        }
    }

    return (
        <div id="search-bar" className="w-120 bg-white rounded-md shadow-lg z-10">
        <form className="flex flex-col items-center justify-center min-h-screen" onSubmit={handleSubmit}>
            <input
            type="text"
            placeholder="Enter your channel name"
            className="w-96 rounded-md px-2 py-1 mb-4 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:border-transparent"
            value={roomName}
            required
            onChange={(e) => setRoomName(e.target.value)}
            />
            <input
            type="password"
            placeholder="Enter your channel password"
            className="w-96 rounded-md px-2 py-1 mb-4 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:border-transparent"
            value={roomPassWord}
            required
            onChange={(e) => setRoomPassWord(e.target.value)}
            onKeyUp={handleKeyUp}
            />
            <div flex space-x-3>
              <button
                type="submit"
                className="bg-gray-800 text-white rounded-md px-4 py-1 ml-2 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:ring-opacity-50"
              >
                Join
              </button>
              <button
                type="button"
                className="bg-gray-800 text-white rounded-md px-4 py-1 ml-2 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:ring-opacity-50"
                onClick={handleCreateRoom}
              >   
                Create 
              </button>
              <button
                type="button"
                className="bg-red-500 text-white rounded-md px-4 py-1 ml-2 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-opacity-50"
                onClick={() => {
                    localStorage.clear();
                    navigate("/login")
                }}
              >
                Logout
              </button>
            </div>
        </form>

        </div>
    );
};

export default Home;
