import React, { useState } from 'react';
import './App.css';

function App() {
  const [modalActive, setModalActive] = useState(null);

  const openModal = (id) => {
    setModalActive(id);
  };

  const closeModals = () => {
    setModalActive(null);
  };

  const switchModal = (id) => {
    setModalActive(id);
  };

  return (
    <div className="App">
      <nav>
        <div className="logo">CLASSIFICATION OF <span>SLEEP DISORDERS</span></div>
        <div className="nav-links">
          <a href="/">HOME</a>
          <a href="#about">ABOUT</a>
          <a href="#" onClick={(e) => { e.preventDefault(); openModal('regModal'); }}>REGISTER</a>
          <a href="#" onClick={(e) => { e.preventDefault(); openModal('loginModal'); }}>LOGIN</a>
          <a href="/admin-login" className="admin-btn">ADMIN</a>
        </div>
      </nav>

      <section className="hero">
        <h1>AN ENSEMBLE LEARNING APPROACH FOR IMPROVED <span> SLEEP DISORDER PREDICTION</span></h1>
      </section>

      <section id="about" className="about-section">
        <div className="about-image">
          <img src="https://images.unsplash.com/photo-1551076805-e1869033e561?q=80&w=2070&auto=format&fit=crop" alt="Sleep Study" />
        </div>
        <div className="about-text">
          <h2>About</h2>
          <div style={{ marginBottom: '60px', color: '#d1d1d1', fontSize: '1.05rem', textAlign: 'justify' }}>
            <p style={{ marginTop: '10px', fontSize: '0.95rem', color: '#ccc' }}>
              Our platform utilizes a <strong>Multi-Model Ensemble</strong> technique. By processing data through <strong>Artificial Neural Networks (ANN)</strong>, we simulate human-like pattern recognition to detect subtle irregularities in sleep cycles. Simultaneously, <strong>Random Forest</strong> and <strong>Support Vector Machines (SVM)</strong> handle high-dimensional physiological data to ensure that factors like blood pressure and stress levels are weighted accurately, reducing the margin of error significantly compared to traditional manual screening.
            </p>
          </div>
        </div>
      </section>

      {modalActive && <div className="overlay" onClick={closeModals}></div>}

      {modalActive === 'regModal' && (
        <div className="modal">
          <h2>Register</h2>
          <form action="/register" method="POST">
            <input type="text" name="name" placeholder="Full Name" required />
            <input type="email" name="email" placeholder="Email Address" required />
            <input type="tel" name="phone" placeholder="Phone Number (10 digits)" 
                   pattern="[0-9]{10}" title="Please enter exactly 10 digits" required />
            <input type="password" name="password" 
                   placeholder="Password (Min 8 chars, 1 Num, 1 Symbol)" 
                   pattern="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
                   title="Must be at least 8 characters, include a letter, a number, and a symbol (@$!%*#?&)"
                   required />
            <button type="submit" className="submit-btn">CREATE ACCOUNT</button>
          </form>
          <div className="switch-text">Already have an account? <a href="#" onClick={(e) => { e.preventDefault(); switchModal('loginModal'); }}>Login</a></div>
        </div>
      )}

      {modalActive === 'loginModal' && (
        <div className="modal">
          <h2>Login</h2>
          <form action="/login" method="POST">
            <input type="email" name="email" placeholder="Email Address" required />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit" className="submit-btn">LOG IN</button>
          </form>
          <div className="switch-text">New user? <a href="#" onClick={(e) => { e.preventDefault(); switchModal('regModal'); }}>Register</a></div>
        </div>
      )}
    </div>
  );
}

export default App;
