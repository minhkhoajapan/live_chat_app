import React, { useState, useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const Chatroom = () => {
    const {roomName} = useParams()
    const navigate = useNavigate()
    const [messages, setMessages] = useState([])
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

      chatSocket.current.onmessage = (e) => {
        const data = JSON.parse(e.data)
        console.log("Hello this is data: ",data)
        setMessages(prevMessages => [...prevMessages, data])
      }

      chatSocket.current.onclose = (e) => {
        console.error('Chat socket closed unexpectedly')
      }

      return () => {
        chatSocket.current.close()
      }

    }, [roomName])

    //scroll the chat to the bottom
    useEffect(() => {
      chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight
    }, [messages])

    const handleSendMessage = (e) => {
      const message = messageInputRef.current.value
      chatSocket.current.send(JSON.stringify({
        'message': message,
        'sender_username': localSender
      }))
      messageInputRef.current.value = ""

    }

    const handleKeyUp = (e) => {
        if (e.keyCode === 13) {
            handleSendMessage()
        }
    }

    return (
      <>
      <div className="h-screen flex flex-col">
        <div className="bg-gray-200 flex-1 overflow-y-scroll">
          <div class="px-4 py-2" ref={chatLogRef}>
          {messages.map((msg, index) => (
          <div key={index} className={`mb-2 ${msg.sender.username === localSender ? 'flex justify-end' : 'flex items-center'}`}>
          {msg.sender.username !== localSender && (
          <>
            <div className="font-medium mr-2">{msg.sender.username}</div>
            <div className="bg-white rounded-lg p-2 shadow max-w-sm">
              {msg.message}
            </div>
          </>
          )}
          {msg.sender.username === localSender && (
          <div className="bg-blue-500 text-white rounded-lg p-2 shadow max-w-sm">
            {msg.message}
          </div>
        )}
        </div>
         ))}
          </div>
        </div>
        <div className="bg-gray-100 px-4 py-2">
          <div className="flex items-center">
            <input className="w-full border rounded-full py-2 px-4 mr-2" type="text" ref={messageInputRef} onKeyUp={handleKeyUp} />
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-full" onClick={handleSendMessage} >
              Send
            </button>
          </div>
        </div>
      </div>
      </>
    );
};

export default Chatroom;
