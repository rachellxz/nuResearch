import React, { useState, useEffect } from "react";
import Categories from "./Categories";
import Login from "./Login";
import "./static/app.css";
import axios from "axios";

const Header = () => {

  const [loggedIn, setLoggedIn] = useState(false);
  const [tab, setTab] = useState('Category')
  useEffect(() => {
    // Update the document title using the browser API
    axios.get('/login')
      .then((res) => { setLoggedIn(res.data) })

  }, []);

  const handleCatClick = () => {
    setTab("Category")
  }

  const handleFeedClick = () => {
    setTab("Feed")
  }

  const tabs = () => {
    return (
      <>
        <nav class="navbar" role="navigation" aria-label="main navigation">
          <div class="navbar-brand">
            <a class="navbar-item" href="#">
              <img src="nuResearch.png" width="200" height="50" />
            </a>
          </div>
        </nav>

        <div className="tabs is-large is-centered">
          <ul>
            <li><a onClick={handleCatClick}>Category</a></li>
            <li><a onClick={handleFeedClick}>Feed</a></li>
          </ul>
        </div>
      </>

    )
  }
  return (
    <>
      <div className="main-content">

        {loggedIn === false ?
          <Login setLoggedIn={setLoggedIn} />
          :

          <>
            {tabs()}
            {tab === 'Category' ?
              <div> <Categories /> </div>
              :
              <div></div>
            }
          </>
        }

      </div>
    </>
  );
};

export default Header;
