import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/PaymentPage.css";
import { book, pay } from "../api";

function PaymentPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { film, session, seats, totalPrice } = location.state || {};

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

    try {
      const token = localStorage.getItem("token");
      for (const seat of seats) {
        const response = await book({
          showtime_id: Number(session.id),
          row_number: Number(seat.split("-")[0]),
          place_number: Number(seat.split("-")[1]),
        }, token);

        await pay({
          booking_id: response.id,
          card_number: cardNumber,
          card_holder: cardHolder,
          cvv: cvv,
        }, token);
      }

      alert("Оплата прошла успешно!");
      navigate("/");
    } catch (exception) {
      alert(`Ошибка при оплате: ${exception}`);
    }
  };

  return (
    <div className="payment-page">
      <h2>Оплата билетов</h2>

      <div className="order-summary">
        <h3>{film.name}</h3>
        <p>Сеанс: {new Date(session.datetime).toLocaleString("ru-RU")}</p>
        <p>Выбранные места: {seats.join(", ")}</p>
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
          placeholder="SURNAME NAME"
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
