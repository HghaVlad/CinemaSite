import { Link } from "react-router-dom";
import "../styles/Header.css";

function Header() {
  if (!localStorage.getItem("token"))
  {
    return (
      <div className = "header">
        <div className = "navigation">
          <div className="navigation-list">
            <div className="navigation-item"><Link to="/">Главная</Link></div>
            <div className="navigation-item"><Link to="/schedule">Афиша</Link></div>
            {/* <div className="navigation-item"><Link to="/about">О нас</Link></div>
            <div className="navigation-item"><Link to="/contacts">Контакты</Link></div> */}
            <div className="navigation-item"><Link to="/profile">Профиль</Link></div>
            <div className="navigation-item"><Link to="/auth">Вход/Регистрация</Link></div>
          </div>
        </div>
      </div>
    );
  }

  else
  {
    return (
      <div className = "header">
        <div className = "navigation">
          <div className="navigation-list">
            <div className="navigation-item"><Link to="/">Главная</Link></div>
            <div className="navigation-item"><Link to="/schedule">Афиша</Link></div>
            <div className="navigation-item"><Link to="/profile">Профиль</Link></div>
          </div>
        </div>
      </div>
    );
  }
}

export default Header;
