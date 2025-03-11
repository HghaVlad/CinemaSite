import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home"; 
import MoviePage from "./pages/MoviePage"
import Header from "./components/Header";
import SeatSelectionPage from "./pages/SeatSelectionPage"
import PaymentPage from "./pages/PaymentPage"
import AuthPage from "./pages/AuthPage"
import RegistrationPage from "./pages/RegistrationPage"
import UserProfilePafe from "./pages/UserProfilePage"
import SchedulePage from "./pages/SchedulePage"
import AboutUsPage from "./pages/AboutUsPage"
import ContactsPage from "./pages/ContactsPage"
import Footer from "./components/Footer"

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/movie/:id" element={<MoviePage />} />
        <Route path="/seats/:id" element={<SeatSelectionPage/>} />
        <Route path="/payment" element={<PaymentPage/>} />
        <Route path="/auth" element = {<AuthPage/>} />
        <Route path="/registration" element = {<RegistrationPage/>} />
        <Route path="/profile" element = {<UserProfilePafe/>}/>
        <Route path="/schedule" element={<SchedulePage/>}/>
        <Route path="/about" element={<AboutUsPage/>}/>
        <Route path="/contacts" element={<ContactsPage/>}/>
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
