import React, { useState, useEffect } from "react";
import { render } from 'react-dom';
import { ThemeProvider } from "@chakra-ui/core";

import Header from "./Components/Header";
import Todos from "./Components/Todos";
import axios from 'axios'

function App() {
  return (
    <>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css" />
      <Header />
    </>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)
