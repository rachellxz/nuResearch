import React, { useState, useEffect } from "react";
import Categories from "./Categories";
import "./static/app.css";
import axios from "axios";

const Header = () => {
  const [isLogin, setIsLogin] = useState(false)
  const [emailInput, setEmailInput] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    // Update the document title using the browser API
    axios.get('/login')
      .then((res) => { console.log(res.data); setIsLogin(res.data) })

  });

  const updateEmail = e => {
    setEmailInput(e.target.value);
  }

  const saveEmail = async (e) => {
    e.preventDefault();
    setLoggedIn(true);

    await axios.post('/login', {
      name: emailInput
    })
      .then(function (response) {
        console.log(response);
      })
  }

  return (
    <div className="main">
      <h1> nuResearch </h1>

      {loggedIn === true ?
        <div>
          <h2> What's your email? </h2>
          <form onSubmit={saveEmail}>
            <input type="email" id="email" name="email" onChange={updateEmail} required />
            <input type="submit" id="submit-btn" value="Next" />
          </form>
        </div>
        :
        <div> <Categories /> </div>
      }

    </div>
  );
};

export default Header;
