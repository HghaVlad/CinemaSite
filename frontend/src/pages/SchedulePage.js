import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "../styles/SchedulePage.css"
import {showtimes, films} from "../api";
function SchedulePage() 
{
  const [selectedMovie, setSelectedMovie] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [movies, setMovies] = useState([]);
  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    const getFilms = async () => {
      try {
        const response = await films();
        if (response.films) {
          setMovies(response.films);
        } else {
          console.error("Ошибка при загрузке фильмов:", response);
        }
      } catch (error) {
        console.error("Ошибка при получении фильмов:", error);
      }
    };

    const getSchedule = async () => {
      try {
        const response = await showtimes();
        if (response.showtimes) {
          setSchedule(response.showtimes);
        } else {
          console.error("Ошибка при загрузке расписания:", response);
        }
      } catch (error) {
        console.error("Ошибка при получении расписания:", error);
      }
    };


    getFilms();
    getSchedule();
  }, []);


  const filteredSchedule = schedule.filter((session) => {
    const isMovieMatch = !selectedMovie || session.film_id === Number(selectedMovie);
  
    const sessionDate = new Date(session.datetime).toISOString().split("T")[0];
    const isDateMatch = !selectedDate || sessionDate === selectedDate;
  
    return isMovieMatch && isDateMatch;
  });

  return (
    <div className="schedule-page">
      <h2>Расписание сеансов</h2>
      <div className="filters">
        <select onChange={(e) => setSelectedMovie(e.target.value)}>
          <option value="">Выберите фильм</option>
          {movies.map((movie) => (
            <option key={movie.id} value={movie.id}>
              {movie.name}
            </option>
          ))}
        </select>

        <input
          type="date"
          onChange={(e) => setSelectedDate(e.target.value)}
        />
      </div>

      <table className="schedule-table">
        <thead>
          <tr>
            <th>Фильм</th>
            <th>Время</th>
            <th>Зал</th>
            <th>Свободные места</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {filteredSchedule.length > 0 ? (
            filteredSchedule.map((session) => {
              const movie = movies.find((m) => m.id === session.film_id);
              return (
                <tr key={session.id}>
                  <td>{movie?.name}</td>
                  <td>{new Date(session.datetime).toLocaleString()}</td>
                  <td>{session.total_rows * session.total_places_per_row - session.booked_seats.length}</td>
                  <td>
                    <Link to={`/seats/${session.id}`}>
                    <button>Выбрать места</button>
                    </Link>
                  </td>
                </tr>
              );
            })
          ) : (
            <tr>
              <td colSpan="5">Нет доступных сеансов</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default SchedulePage;
