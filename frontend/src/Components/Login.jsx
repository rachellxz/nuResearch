import React, { useState, useEffect } from "react";
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
    <div className="main">
      <img src="nuResearch.png" width="300" className="logo-landing" />
      <div className="field">
        <label class="label">What's your email?</label>
        <div class="control">
          <form onSubmit={saveEmail}>
            <input className="input" type="email" id="email" name="email" onChange={updateEmail} required />
            <button className="button" type="submit" id="submit-btn">Next</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
