import React, { useState, useEffect } from "react";
import Categories from "./Categories";
import Login from "./Login";
import "./static/app.css";
import axios from "axios";

const Feed = () => {
  useEffect(() => {
    // Update the document title using the browser API
    axios.get('/login')
      .then((res) => { setLoggedIn(res.data) })

  }, []);


  return (
    <>
    </>
  );
};

export default Feed;
