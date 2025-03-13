import React, { useEffect, useState } from "react"; 
import { useParams, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import "../styles/MoviePage.css";
import { filmId, showtimes } from "../api";

function MoviePage() {
  const { id } = useParams();
  const [film, setFilm] = useState(null);
  const [schedule, setSchedule] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const getFilm = async () => {
      try {
        const response = await filmId(Number(id));
        setFilm(response);
      } catch (exception) {
        alert(`Ошибка при получении данных фильма: ${exception}`);
        navigate("/home");
      }
    };

    const getSessions = async () => {
      try {
        const response = await showtimes();
        setSchedule(response.showtimes.filter(session => session.film_id === Number(id)));
      } catch (exception) {
      }
    };

    getFilm();
    getSessions();
  }, [id, navigate]);

  const formatDuration = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    const hoursText = hours === 1 ? "час" : (hours >= 2 && hours <= 4 ? "часа" : "часов");
    const minsText = mins === 1 ? "минута" : (mins >= 2 && mins <= 4 ? "минуты" : "минут");
  
    return hours > 0 ? mins > 0 ? `${hours} ${hoursText} ${mins} ${minsText}` : `${hours} ${hoursText} ` : `${mins} ${minsText}`;
  };

  return (
    <div className="movie-page">
      {film ? (
        <>
          <div className="movie-content">
            <div className="movie-poster">
              <img src={film.poster_url} alt={film.name} />
            </div>
            <div className="movie-info">
              <h1>{film.name}</h1>
              <p><strong>Жанр:</strong> {film.genre}</p>
              <p><strong>Продолжительность:</strong> {formatDuration(film.duration)}</p>
              <p><strong>Возраст:</strong> {film.age_restriction}+</p>
              <p><strong>Рейтинг IMDb:</strong> {film.imdb_rating}</p>
              <p className="description">{film.description}</p>
            </div>
          </div>

          <div className="movie-schedule">
            <h2>Расписание сеансов</h2>
            {schedule.length > 0 ? (
              <>
                <select onChange={(e) => setSelectedSession(e.target.value)}>
                  <option value="">Выберите сеанс</option>
                  {schedule.map((session) => (
                    <option key={session.id} value={session.id}>
                      {new Date(session.datetime).toLocaleString()}
                      </option>
                  ))}
                </select>
                <Link to={selectedSession ? `/seats/${selectedSession}` : "#"}>
                  <button disabled={!selectedSession}>Купить билет</button>
                </Link>
              </>
            ) : (
              <p>Расписание недоступно</p>
            )}
          </div>
        </>
      ) : (
        <p>Загрузка...</p>
      )}
    </div>
  );
}

export default MoviePage;