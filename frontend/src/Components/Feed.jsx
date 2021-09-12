import React, { useState, useEffect } from "react";
import Categories from "./Categories";
import Login from "./Login";
import "./static/app.css";
import axios from "axios";

const Feed = () => {
  const [channels, setChannels] = useState([])

  useEffect(() => {
    const interval = setInterval(() => {
      await axios.get('/category')
      .then((res) => { setChannels(res.data) })    }, 1000);
    return () => clearInterval(interval);
  }, []);



  return (
    <>
    </>
  );
};

export default Feed;
