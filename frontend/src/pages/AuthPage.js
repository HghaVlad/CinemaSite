import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signIn } from "../api";
import "../styles/AuthPage.css";

function AuthPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");

  if (localStorage.getItem("token"))
  {
    navigate("/profile");
  }
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); 
    try {
      const response = await signIn({
        email: formData.email,
        password: formData.password,
      });

      if (response.detail) {
        alert(`Ошибка: ${response.detail}`);
        return;
      }

      localStorage.setItem("token", response.access_token);
      alert("Авторизация прошла успешно!");
      navigate("/profile");
    } catch (error) {
      alert("Ошибка при авторизации");
      console.error(error);
    }
  }

  return (
    <div className="auth-page">
      <h2>Вход</h2>
      
      <form onSubmit={handleSubmit} className="auth-form">
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Пароль"
          value={formData.password}
          onChange={handleChange}
          required
        />
        
        {error && <p className="error-message">{error}</p>}

        <button type="submit">Войти</button>

        <p className="switch-auth" onClick={() => navigate("/registration")}>
          Нет аккаунта? Зарегистрируйтесь!
        </p>
      </form>
    </div>
  );
}

export default AuthPage;
