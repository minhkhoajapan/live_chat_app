import axios from "axios";
import {ACCESS_TOKEN} from "./constants.js"

const herokuUrl = "https://live-chat-app-minh-khoa-0b52e2a47843.herokuapp.com"

const api = axios.create({
    baseURL: herokuUrl,
})

api.interceptors.request.use(
    (config) => {
        const token =localStorage.getItem(ACCESS_TOKEN)
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default api;
