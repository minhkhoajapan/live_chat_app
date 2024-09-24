import react from "react"
import { useState } from 'react'
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import ChatRoom from "./components/Chatroom"
import ProtectedChatRoom from "./components/ProtectedChatRoom"
import ProtectedRoute from "./components/ProtectedRoute"
import Home from "./pages/Home"
import Login from "./pages/Login"
import Register from "./pages/Register"

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/chat/:roomName" element={<ProtectedRoute><ProtectedChatRoom><ChatRoom /></ProtectedChatRoom></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  )
} 

export default App
