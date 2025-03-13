import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { films } from "../api";
import "../styles/Home.css"

function Home() {
  const [movies, setMovies] = useState([]);
  const navigate = useNavigate();

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

    getFilms();
  }, []);

  return (
    <div className="home">
      <h2>Сейчас в кино</h2>
      <div className="movies-container">
        {movies.length > 0 ? (
          movies.map((movie) => (
            <div 
            key={movie.id}               
            onClick={() => navigate(`/movie/${movie.id}`)}
            className="movie-card">
              <img src={movie.poster_url} alt={movie.name} className="movie-poster" />
              <h3>{movie.name}</h3>
              <p>{movie.genre} | {movie.duration} мин</p>
                          </div>
          ))
        ) : (
          <p>Фильмы загружаются...</p>
        )}
      </div>
    </div>
  );
}

export default Home;
