import React, { useState, useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from "../api.js"
import LocalSenderChat from './LocalSenderChat.jsx';
import OtherSenderChat from './OtherSenderChat.jsx';
import ChatMessageKebabMenu from './ChatMessageKebabMenu.jsx';

const Chatroom = () => {
    const {roomName} = useParams()
    const navigate = useNavigate()
    const [messages, setMessages] = useState([])
    const [selectedFile, setSelectedFile] = useState(null)
    const [activeDropdown, SetActiveDropdow] = useState(null)
    const chatLogRef = useRef(null)
    const messageInputRef = useRef(null)
    const chatSocket = useRef(null)
    const baseURL = "localhost:8000"
    const localSender = localStorage.getItem("username")

    useEffect(() => {
      //Initial chatSocket
      chatSocket.current = new WebSocket(
        `ws://${baseURL}/ws/chat/${roomName}/`
      )

      preloadingMessages().catch() 

      chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight

      chatSocket.current.onmessage = (e) => {
        const data = JSON.parse(e.data)
        if (data.message_deleted) {
          setMessages(prevMessages => prevMessages.filter(msg => msg.id != data.message_deleted))
        } else {
          setMessages(prevMessages => [...prevMessages, data])
          console.log(data)
        }
      }

      chatSocket.current.onclose = async (e) => {
        try {
          await api.post("/api/exit/chatroom/", {
            'username': localSender,
            'room_name': roomName,
          })
        } catch (error) {
          console.log('Error exiting chat room:', error)
        }
      }

      return () => {
        chatSocket.current.close()
      }

    }, [roomName])

    const preloadingMessages = async () => {
      try {
        const res = await api.get(`/api/load/messages/${roomName}/`)
        if (res.status === 200) {
          setMessages(res.data)
        }
      } catch (error) {
        console.log(error)
      }
    }

    const handleSendMessage = (e) => {
      const message = messageInputRef.current.value
      chatSocket.current.send(JSON.stringify({
        'message': message,
        'sender_username': localSender
      }))
      messageInputRef.current.value = ""
    }

    const handleFileChange = (e) => {
      setSelectedFile(e.target.files[0])
    }

    const handleSendFile = async (e) => {
      if (!selectedFile) return
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('sender_username', localSender)
      formData.append('room_name', roomName)
      
      try {
        res = api.post("/api/upload/media/chatroom/", formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        })
      } catch (error) {
        console.error("File upload failed:", error);
      }
    }

    const handleKeyUp = (e) => {
      if (e.keyCode === 13) {
        handleSendMessage()
      }
    }

    const handleExitButton = (e) => {
      navigate("/")
    }

    const toggleDropdown = (index) => {
      SetActiveDropdow(activeDropdown === index ? null : index)
    }

    const handleDeleteMessage = async (index) => {
      const messageId = messages[index].id
      try {
        const res = await api.delete(`/api/delete/message/${messageId}/`)
        if (res.status === 204) {
          //broadcast the delete to the whole group
          chatSocket.current.send(JSON.stringify({
            'message_deleted': messageId,
          }))
        }
      } catch (error) {
        console.log(error)
      }
    }

    return (
      <>
      <div className="h-screen flex flex-col">
        {/* ChatRoom Header */}
        <div className="bg-gray-800 text-white px-4 py-2 flex items-center">
          {/* Left arrow icon */}
          <button className="mr-4" onClick={handleExitButton}>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          <h1 className="text-xl font-bold">{roomName}</h1>
        </div>

        {/* Chat message Area */}
        <div className="bg-gray-200 flex-1 overflow-y-scroll">
          <div class="px-4 py-2" ref={chatLogRef}>
          {messages.map((msg, index) => (
          <div key={index} className={`mb-2 ${msg.sender.username === localSender ? 'flex justify-end' : 'flex items-center'}`}>
          {msg.sender.username !== localSender && (
            <>
              <OtherSenderChat msg={msg} />
              <ChatMessageKebabMenu 
                isLocalSender={false}   
                onToggleDropdown={toggleDropdown}
                isActive={activeDropdown===index}
                index={index}
                onDeleteMessage={handleDeleteMessage}
              />
            </>
          )}
          {msg.sender.username === localSender && (
            <>
              <ChatMessageKebabMenu 
                isLocalSender={true}
                onToggleDropdown={toggleDropdown}
                isActive={activeDropdown===index}
                index={index}
                onDeleteMessage={handleDeleteMessage}
              />  
              <LocalSenderChat msg={msg} />        
            </> 
          )}
        </div>
         ))}
          </div>
        </div>
        {/* Message input and send buttons */}
        <div className="bg-gray-100 px-4 py-2">
          <div className="flex items-center">
            <input className="w-5/6 border rounded-full py-2 px-4 mr-2" type="text" ref={messageInputRef} onKeyUp={handleKeyUp} />
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-full" onClick={handleSendMessage} >
              Send
            </button>

            {/* File upload button */}
            <input type="file" id="fileInput" style={{display: 'none'}} onChange={handleFileChange} />
            <label htmlFor="fileInput" className="bg-gray-500 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-full mr-2 cursor-pointer">
              Choose File
            </label>
            <button
              className="bg-green-500 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-full"
              onClick={handleSendFile}
              disabled={!selectedFile}
            >
              Send File
            </button>
          </div>
        </div>
      </div>
      </>
    );
};

export default Chatroom;
