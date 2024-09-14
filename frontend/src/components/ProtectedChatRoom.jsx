import api from "../api";
import {useState, useEffect} from "react"
import { Navigate, useParams } from "react-router-dom";

function ProtectedChatRoom({children}) {
    const [haveAccess, setHaveAccess] = useState(null)
    const currentUser = localStorage.getItem("username")
    const {roomName} = useParams()

    useEffect(() => {
        checkRoomAccess().catch(() => setHaveAccess(false))
    }, [])

    const checkRoomAccess = async () => {
        try {
            const res = await api.post("/api/validation/user/chatroom/", {
                "username": currentUser,
                "room_name": roomName
            })
            if (res.status === 200 ) {
                setHaveAccess(true)
            } else {
                setHaveAccess(false)
            }
        } catch (error) {
            console.log(error)
            setHaveAccess(false)
        }
    }

    if (haveAccess === null) {
        return <div>Loading...</div>
    }

    return haveAccess ? children : <Navigate to="/" />

}