import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { me, changeUser, history } from "../api";

function UserProfilePage() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const [editing, setEditing] = useState(false);
  const [orders, setOrders] = useState([]);
  const handleLogout = () => {
    localStorage.removeItem("token");
    alert("Вы вышли из аккаунта");
    navigate("/auth");
  };

  useEffect(() => {
    const getUser = async () => {
      const token = localStorage.getItem("token");
      console.log("Токен в localStorage:", token); 


      if (!token)
      {
        navigate("/auth");
      }
      try {
        const responce = await me(token);
        if (!responce) {
          console.error("Респонс не ок");
          navigate("/auth");
          return;
        }

        setUser(responce);
      } catch (error) {
        console.error("Ошибка при получении данных:", error);
        localStorage.removeItem("token");
        navigate("/auth");
      }
    };

    const getOrders = async () => {
      const token = localStorage.getItem("token"); 

      if (!token)
      {
        navigate("/auth");
      }
      try {
        const responce = await history(token);
        if (!responce) {
          console.error("Респонс не ок");
          navigate("/auth");
          return;
        }

        setOrders(responce);
      } catch (error) {
      }
    };

    getUser();
    getOrders();
  }, [navigate]);


  const toggleEdit = async () => {
    if (editing) {
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        const updatedUser = await changeUser(token, {name: user.name, surname: user.surname, email: user.email});
        setUser(updatedUser); 
        alert("Данные успешно сохранены!");
      } catch (error) {
        console.error("Ошибка при обновлении данных:", error);
        alert("Ошибка при сохранении данных.");
      }
      navigate("/profile");
    }

    setEditing(!editing);
  };


  return (
      <div className="profile-page">
        <h2>Профиль пользователя</h2>
    
        {user ? (
          <div className="profile-info">
            <p>
              <strong>Имя:</strong>{" "}
              {editing ? (
                <input
                  type="text"
                  value={user.name}
                  onChange={(e) => setUser({ ...user, name: e.target.value })}
                />
              ) : (
                user.name
              )}
            </p>
            <p>
              <strong>Фамилия:</strong>{" "}
              {editing ? (
                <input
                  type="text"
                  value={user.surname}
                  onChange={(e) => setUser({ ...user, surname: e.target.value })}
                />
              ) : (
                user.surname
              )}
            </p>
            <p>
              <strong>Email:</strong>{" "}
              {editing ? (
                <input
                  type="email"
                  value={user.email}
                  onChange={(e) => setUser({ ...user, email: e.target.value })}
                />
              ) : (
                user.email
              )}
            </p>
            {editing ? (
              <button onClick={toggleEdit}>Сохранить</button>
            ) : (
              <button onClick={toggleEdit}>Редактировать</button>
            )}
          </div>
        ) : (
          <p>Загрузка данных...</p>
        )}
    
        <h3>История покупок</h3>
        <ul className="purchase-history">
          {orders.map((order) => (
            <p className="switch-auth" onClick={() => order.ticket_url}>
              <a href={order.ticket_url} target="_blank" rel="noreferrer">
            {order.film_title} – {order.datetime}
            </a>
          </p>
          ))}
        </ul>
    
        <button className="logout-button" onClick={handleLogout}>
          Выйти из аккаунта
        </button>
      </div>
    );
}

export default UserProfilePage;
