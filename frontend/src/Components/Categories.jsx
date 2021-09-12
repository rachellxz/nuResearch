import React, { useState, useEffect } from "react";
import axios from "axios";
import "./static/app.css";

const Categories = () => {
    const [categories, setCategories] = useState([]);
    const [isClicked, setIsClick] = useState(false)
    const [category, setCategory] = useState('Select A Category')

    useEffect(() => {
        // Update the document title using the browser API
        axios.get('/channels')
            .then((res) => { setCategories(res.data) });
    }, [])

    const handleClick = () => {
        setIsClick(!isClicked);
    }

    const handleCatClick = (cat) => {
        setIsClick(false)
        setCategory(cat)
    }



    const handleSubmit = async () => {
        setIsClick(false)
        await axios.post('/category', {
            "category": category
        })
        console.log(category)
    }

    return (

        <>
            {isClicked ?
                <div className="dropdown is-active">
                    <div className="dropdown-trigger" onClick={handleClick}>
                        <button className="button" aria-haspopup="true" aria-controls="dropdown-menu">
                            <span>{category}</span>
                            <span className="icon is-small">
                                <i className="fas fa-angle-down" aria-hidden="true"></i>
                            </span>
                        </button>
                    </div>
                    <div className="dropdown-menu" id="dropdown-menu" role="menu">
                        <div className="dropdown-content">
                            {
                                categories.map(cat => {
                                    return (
                                        <>
                                            <a href="#" onClick={(e) => { handleCatClick(cat) }} className="dropdown-item">
                                                {cat}
                                            </a>
                                        </>
                                    )
                                })
                            }
                        </div>
                    </div>
                    <button onClick={handleSubmit} className="button"> Submit </button>

                </div> :

                <div className="dropdown">
                    <div className="dropdown-trigger" onClick={handleClick}>
                        <button className="button" aria-haspopup="true" aria-controls="dropdown-menu">
                            <span> {category} </span>
                            <span className="icon is-small">
                                <i className="fas fa-angle-down" aria-hidden="true"></i>
                            </span>
                        </button>
                    </div>

                    <button onClick={handleSubmit} className="button"> Submit </button>

                </div>


            }

        </>
    )
}

export default Categories;