import React, { useState, useEffect } from "react";
import "./static/app.css";
import axios from "axios";

const Feed = () => {
  const [channels, setChannels] = useState([])
  const [news, setNews ] = useState([])

  const handleChannels = async (channels) => {
    let newsToUpdate = [] 
    for (const channel in channels) {
      const news_res = await axios.post('/news', {"name": channels[channel], "size": 20})
      console.log(news_res)
      newsToUpdate = [...newsToUpdate, ...news_res.data]
    }
    setNews(newsToUpdate)
  }

  useEffect(() => {
    const interval = setInterval(async () => {
      const user_channels = await axios.get('/category')
      setChannels(user_channels.data)
      await handleChannels(user_channels.data)

    }, 1000);

    return () => {
      clearInterval(interval);
    };
  });

  console.log(channels)

  return (
    <>
    <div className = "columns"> 
      <div className = "column"/>
      <div className = "column">
      {
        news.map((elem, idx) => {
          console.log(idx)
          if (elem.image !== '' && idx % 2 === 0) {
            return(
            <>
            <div class="card">
            <header class="card-header">
              <p class="card-header-title">
                {elem.title}
              </p>
            </header>
            <div class="card-image">
              <figure class="image is-4by3">
                <img src={elem.image} alt="Placeholder image"/>
              </figure>
            </div>
            <div class="content">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
              Phasellus nec iaculis mauris. <a>@bulmaio</a>.
              <a href="#">#css</a> <a href="#">#responsive</a>
              <br/>
            </div>
          </div> 
          <br/>
          </>
          )
        }})
      }
      </div>

      <div className = "column">
      {
        news.map((elem, idx) => {
          console.log(idx)
          if (elem.image !== '' && idx % 2 === 1) {
            return(
            <>
            <div class="card">
            <header class="card-header">
              <p class="card-header-title">
                {elem.title}
              </p>
            </header>
            <div class="card-image">
              <figure class="image is-4by3">
                <img src={elem.image} alt="Placeholder image"/>
              </figure>
            </div>
            <div class="content">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
              Phasellus nec iaculis mauris. <a>@bulmaio</a>.
              <a href="#">#css</a> <a href="#">#responsive</a>
              <br/>
            </div>
          </div>
          <br/> 
          </>
          )
        }})
      }

      </div>
      <div className = "column"/>
    </div>

    </>
  );
};

export default Feed;
