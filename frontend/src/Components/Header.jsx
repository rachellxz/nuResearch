import React, { useState, useEffect } from "react";
import Categories from "./Categories";
import Login from "./Login";
import "./static/app.css";
import axios from "axios";

const Header = () => {

  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    // Update the document title using the browser API
    axios.get('/login')
      .then((res) => { setLoggedIn(res.data) })

  });


  return (
    <div className="main">
      <h1> nuResearch </h1>

      {loggedIn === false ?
        <Login setLoggedIn={setLoggedIn} />
        :
        <div> <Categories /> </div>
      }

    </div>
  );
};

export default Header;
