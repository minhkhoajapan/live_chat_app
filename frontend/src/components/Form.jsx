import { useState } from "react";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import { useNavigate } from "react-router-dom";

function Form({method, route}) {
    const formName = method === "login" ? "Login" : "Register"
    const isRegister = method === "register" 

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [passwordErrors, setPasswordErrors] = useState({})
    const navigate = useNavigate()

    const passwordValidation = () => {
      const errorFound = {}
      const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/

      if (!passwordRegex.test(password)) {
        errorFound.password = "password must contain at least 8 characters, one letter, one number, and one special character"
      }

      if (password !== confirmPassword) {
        errorFound.confirmPassword = "Passwords do not match"
      } 

      setPasswordErrors(errorFound)
      return Object.keys(errorFound).length === 0
    }

    const handleRegister = async () => {
      const isValid = passwordValidation()
      if (!isValid) return

      try {
        const res = await api.post(route, {username, password})
        navigate("/login")
      } catch (error) {
        console.log(error)
        alert(error)
      }
    }

    const handleLogin = async () => {
      try {
        const res = await api.post(route, {username, password})
        localStorage.setItem(ACCESS_TOKEN, res.data.access)
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh)
        localStorage.setItem("username", username)
        navigate("/")
      } catch (error) {
        console.log(error)
        alert(error)
      }
    }

    const handleSubmit = async (e) => {
      e.preventDefault()
      if (method === "login") {
        await handleLogin()
      } else {
        await handleRegister()
      }
    }

    return (
        <div className="container px-4 mx-auto">
            
          <div className="max-w-lg mx-auto">
            <div className="text-center mb-6">
              <h2 className="text-3xl md:text-4xl font-extrabold">{formName}</h2>
            </div>
            <form action="">
              <div className="mb-6">
                <label className="block mb-2 font-extrabold" htmlFor="username">User Name</label>
                <input
                  className="inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 bg-white shadow border-2 border-indigo-900 rounded"
                  type="text"
                  id="username"
                  value={username}
                  placeholder=""
                  required
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div className="mb-6">
                <label className="block mb-2 font-extrabold" htmlFor="password">Password</label>
                {passwordErrors.password && (
                  <p className="text-red-500 text-sm mb-2">{passwordErrors.password}</p>
                )}
                <input
                  className="inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 bg-white shadow border-2 border-indigo-900 rounded"
                  type="password"
                  id="password"
                  value={password}
                  required
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>      

              {isRegister && (
                <div className="mb-6">
                  <label className="block mb-2 font-extrabold" htmlFor="confirmpassword">Confirm Password</label>
                  {passwordErrors.confirmPassword && (
                    <p className="text-red-500 text-sm mb-2">{passwordErrors.confirmPassword}</p>
                  )}
                  <input
                    className="inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 bg-white shadow border-2 border-indigo-900 rounded"
                    type="password"
                    id="confirmpassword"
                    value={confirmPassword}
                    required
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                </div> 
              )}  

              <div className="flex flex-wrap -mx-4 mb-6 items-center justify-between">
                <div className="w-full lg:w-auto px-4 mb-4 lg:mb-0">
                  <label htmlFor="remember-me">
                    <input type="checkbox" id="remember-me" />
                    <span className="ml-1 font-extrabold">Remember me</span>
                  </label>
                </div>
                <div className="w-full lg:w-auto px-4">
                  <a className="inline-block font-extrabold hover:underline" href="#">Forgot your password?</a>
                </div>
              </div>
              <button
                type="submit"
                className="inline-block w-full py-4 px-6 mb-6 text-center text-lg leading-6 text-white font-extrabold bg-indigo-800 hover:bg-indigo-900 border-3 border-indigo-900 shadow rounded transition duration-200"
                onClick={handleSubmit}
              >
                {formName}
              </button>
              <p className="text-center font-extrabold">
                {isRegister ? "Have" : "Don't have"} an account? <a className="text-red-500 hover:underline" href={isRegister? "/login" : "/register"}>Sign {isRegister ? "in" : "up"}</a>
              </p>
            </form>
          </div>
        </div>
      );
}

export default Form