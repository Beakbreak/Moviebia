import React from 'react'
import classes from './Banner.module.scss'
import { useCallback, useState, useEffect } from 'react'
import { Link } from 'react-router-dom';
function BannerChild(props) {

    const [movieData, setMovieData] = useState({});

    // const fetchDetails = useCallback(async () => {
    //     const response = await fetch(`https://api.themoviedb.org/3/movie/${props.movieId}?api_key=4b11b7e0cdfd1a7257e990731db91e96`)
    //     if (!response.ok) {
    //         throw new Error('Something went wrong');
    //     }
    //     const data = await response.json();
    //     // console.log(data);
    //     setMovieData(data)
    // }, [props.movieId])

    // useEffect(() => {
    //     fetchDetails();
    // }, [fetchDetails])

    const { movie } = props;

    // const year = new Date(movieData.release_date).getFullYear();
    // const lang = (movieData.original_language).toUpperCase();

    return (
        <div className={classes["img-shadow"]}>
            <img src={`http://image.tmdb.org/t/p/w500${movie.backdrop_path}`} className={classes.bannerImage} />
            <div className={classes.movInfo}><h2 className={classes.movName}>{movie.title}</h2>
                <h3 className={classes.movProps}></h3><div className={classes.plot}>{movie.overview}</div><Link to="/Dashboard/Movie"><button className={classes.btn} >Learn More / Rate Now</button></Link></div>
        </div>
    )
}

export default BannerChild