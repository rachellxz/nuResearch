import React, { useState, useEffect } from "react";
import Categories from "./Categories";
import axios from "axios";

const Login = (props) => {
  const [emailInput, setEmailInput] = useState("");


  const updateEmail = e => {
    setEmailInput(e.target.value);
  }

  const saveEmail = async (e) => {
    e.preventDefault();
    props.setLoggedIn(true);

    await axios.post('/login', {
      name: emailInput
    })
      .then(function (response) {
        console.log(response);
      })
  }

  return (
    <>
      <div>
        <h2> What's your email? </h2>
          <form onSubmit={saveEmail}>
            <input type="email" id="email" name="email" onChange={updateEmail} required />
            <input className = "button" type="submit" id="submit-btn" value="Next" />
          </form>
      </div>
    </>
  );
};

export default Login;
