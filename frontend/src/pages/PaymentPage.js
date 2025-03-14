import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/PaymentPage.css";
import { pay } from "../api";

function PaymentPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { film, session, tickets, totalPrice } = location.state || {};

  const [cardNumber, setCardNumber] = useState("");
  const [cardHolder, setCardHolder] = useState("");
  const [cvv, setCvv] = useState("");

  if (!localStorage.getItem("token"))
    {
      alert("Для оплаты необходимо авторизироваться на сайте");
      navigate("/auth");
    }

  const handlePayment = async (e) => {
    e.preventDefault();

      const token = localStorage.getItem("token");
      let isOk = false;
      let isNotificated = false;
      console.log(tickets[0])
      for (const ticket of tickets) {
        try
        {
            const payResponse = await pay({
            booking_id: ticket,
            card_number: cardNumber,
            card_holder: cardHolder,
            cvv: cvv,
          }, token);
          console.log(payResponse)
          if(payResponse.status === "success" && !isNotificated)
          {
            alert("Оплата прошла успешно!");
            isNotificated = true;
            isOk = true;
          }
          else{
            console.log("Hehe")
            console.log(payResponse)
            console.log(isNotificated)
        if (payResponse.status === "failed" && !isNotificated) {
          alert("Оплата не прошла");
          isNotificated = true;
        }
      
        else if (payResponse.status === "not_enough_money" && isNotificated) {
          alert("На карте недостаточно средств");
          isNotificated = true;
        }
      
        else if (payResponse.detail === "Booking not found" && isNotificated) {
          alert("Ошибка: бронирование не найдено");
          isNotificated = true;
        }
        else if (isNotificated == false){
          alert(`Ошибка при оплате`);
          isNotificated = true;
        }
        console.log(isNotificated)
          }
      }

       catch (exception) {
        const errorDetail = exception?.response?.data;
        console.log(errorDetail)
        console.log(exception)
        console.log(exception?.response)
        console.log(isNotificated)
        if (errorDetail.status === "failed" && !isNotificated) {
          alert("Оплата не прошла");
          isNotificated = true;
        }
      
        else if (errorDetail.status === "not_enough_money" && isNotificated) {
          alert("На карте недостаточно средств");
          isNotificated = true;
        }
      
        else if (errorDetail.detail === "Booking not found" && isNotificated) {
          alert("Ошибка: бронирование не найдено");
          isNotificated = true;
        }
        else if (isNotificated == false){
          alert(`Ошибка при оплате: ${exception.message || exception}`);
          isNotificated = true;
        }
        console.log(isNotificated)
        
      }
      }

      
    navigate("/");
    
  };

  return (
    <div className="payment-page">
      <h2>Оплата билетов</h2>

      <div className="order-summary">
        <h3>{film.name}</h3>
        <p>Сеанс: {new Date(session.datetime).toLocaleString("ru-RU")}</p>
        <p>Общая стоимость: {totalPrice} ₽</p>
      </div>

      <form onSubmit={handlePayment} className="payment-form">
      <label for="ccn">Номер карты:</label>
      <input
          type="text"
          placeholder="**** **** **** ****"
          value={cardNumber}
          onChange={(e) => setCardNumber(e.target.value)}
          required
        />

        <label>Владелец карты:</label>
        <input
          type="text"
          placeholder="FULLNAME"
          value={cardHolder}
          onChange={(e) => setCardHolder(e.target.value)}
          required
        />

        <label>CVV:</label>
        <input
          type="password"
          placeholder="***"
          value={cvv}
          onChange={(e) => setCvv(e.target.value)}
          required
        />

        <p className="secure-message">🔒 Ваш платеж защищён</p>

        <button type="submit">Оплатить</button>
      </form>
    </div>
  );
}

export default PaymentPage;
