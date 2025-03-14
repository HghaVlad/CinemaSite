import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "../styles/SeatSelectionPage.css";
import { showtime, filmId, book } from "../api";

function SeatSelectionPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [session, setSession] = useState(null);
  const [film, setFilm] = useState(null);
  const [bookedSeats, setBookedSeats] = useState([]);

  useEffect(() => {
    const getShowtime = async () => {
      try {
        const response = await showtime(Number(id));
        setSession(response);
        if (response.booked_seats?.length > 0) {
          setBookedSeats(response.booked_seats.map(seat => `${seat.row - 1}-${seat.place - 1}`));
        }
      } catch (exception) {
        console.error("Ошибка при получении сеанса:", exception);
        navigate("/");
      }
    };

    getShowtime();
  }, [id, navigate]);

  useEffect(() => {
    if (!session?.film_id) return;

    const getFilm = async () => {
      try {
        const response = await filmId(Number(session.film_id));
        setFilm(response);
      } catch (exception) {
        console.error("Ошибка при получении фильма:", exception);
      }
    };

    getFilm();
  }, [session?.film_id]);

  if (!session) return <p>Загрузка сеанса...</p>;
  if (!film) return <p>Загрузка фильма...</p>;

  const seatsData = Array(session.total_rows)
    .fill()
    .map(() => Array(session.total_places_per_row).fill(false));

  const toggleSeat = (row, col) => {
    const seatId = `${row}-${col}`;
    if (bookedSeats.includes(seatId)) return;
    setSelectedSeats(prev =>
      prev.includes(seatId) ? prev.filter(s => s !== seatId) : [...prev, seatId]
    );
  };

  const totalPrice = selectedSeats.length * parseInt(session.price || 0);

  const goToPayment = async() => {
    let bookingIds = [];

    if (selectedSeats.length > 0) {
      if (!localStorage.getItem("token"))
        {
          alert("Для оплаты необходимо авторизироваться на сайте");
          navigate("/auth");
          return;
        }

        try {
          const token = localStorage.getItem("token");
                    for (const seat of selectedSeats) {
            const response = await book({
              showtime_id: Number(session.id),
              row_number: Number(seat.split("-")[0]) + 1,
              place_number: Number(seat.split("-")[1]) + 1,
            }, token);

            bookingIds.push(response.id);
          }
        }
        catch(exception)
        {
          alert(`Ошибка при бронировании: ${exception}`);
          navigate("/");
        }
      navigate("/payment", {
        state: {
          film: film,
          session: session,
          tickets: bookingIds,
          totalPrice: totalPrice,
        },
      });
    }
  };

  return (
    <div className="seat-selection-page">
      <h2>Выбор мест</h2>
      <p>Сеанс: {film.name} - {new Date(session.datetime).toLocaleString("ru-RU")}</p>

      <div className="screen">Экран</div>
      <div className="seating">
        {seatsData.map((row, rowIndex) => (
          <div key={rowIndex} className="seat-row">
            {row.map((_, colIndex) => {
              const seatId = `${rowIndex}-${colIndex}`;
              const isBooked = bookedSeats.includes(seatId);
              return (
                <div
                  key={seatId}
                  className={`seat ${isBooked ? "booked" : selectedSeats.includes(seatId) ? "selected" : ""}`}
                  onClick={() => toggleSeat(rowIndex, colIndex)}
                >
                  {colIndex + 1}
                </div>
              );
            })}
            <span className="row-number">{rowIndex + 1}</span>
          </div>
        ))}
      </div>

      <p>Выбрано мест: {selectedSeats.length}</p>
      <p>Общая стоимость: {totalPrice} ₽</p>

      <button onClick={goToPayment} disabled={selectedSeats.length === 0}>
        Перейти к оплате
      </button>
    </div>
  );
}

export default SeatSelectionPage;
