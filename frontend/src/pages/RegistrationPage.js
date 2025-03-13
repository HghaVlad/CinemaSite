import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signUp } from "../api";
import "../styles/RegistrationPage.css";

function RegistrationPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    surname: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  if (localStorage.getItem("token"))
    {
      navigate("/profile");
    }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      alert("Пароли не совпадают!");
      return;
    }

    try {
      const response = await signUp({
        name: formData.name,
        surname: formData.surname,
        email: formData.email,
        password: formData.password,
      });

      if (response.detail) {
        alert(`Ошибка: ${response.detail}`);
        return;
      }

      alert("Регистрация прошла успешно!");
      navigate("/auth");
    } catch (error) {
      alert(`Ошибка при регистрации: ${error}`);
      console.error(error);
    }
  };

  return (
    <div className="reg-page">
      <h2>Регистрация</h2>
      
      <form onSubmit={handleSubmit} className="reg-form">
        <input type="text" name="name" placeholder="Имя" value={formData.name} onChange={handleChange} required />
        <input type="text" name="surname" placeholder="Фамилия" value={formData.surname} onChange={handleChange} required />
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
        <input type="password" name="password" placeholder="Пароль" value={formData.password} onChange={handleChange} required />
        <input type="password" name="confirmPassword" placeholder="Повторите пароль" value={formData.confirmPassword} onChange={handleChange} required />

        <button type="submit">Зарегистрироваться</button>

        <p className="registration" onClick={() => navigate("/auth")}>
          Уже есть аккаунт? Войдите!
        </p>
      </form>
    </div>
  );
}

export default RegistrationPage;
