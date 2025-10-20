import { Link } from "react-router-dom";
import "../styles/Header.css";

function Header() {
    return (
      <div className = "header">
        <div className = "navigation">
          <div className="navigation-list">
            <div className="navigation-item"><Link to="/">Главная</Link></div>
            <div className="navigation-item"><Link to="/schedule">Афиша</Link></div>
            <div className="navigation-item"><Link to="/profile">Профиль</Link></div>
          </div>
        </div>
      </div>)
}

export default Header;
