
import Banner from './Banner';
import Navmenu from './Navmenu';
import classes from './Dashboard.module.scss';
import ContentSlider from './ContentSlider';

const Dashboard = () => {
    return (<>

        <div className={classes["background-container"]}>
        </div>
        <Navmenu />
        <Banner endpoint="trending" />

        <ContentSlider title="Suggested For You" endpoint="suggestions" />
        <ContentSlider title="Most Rated" endpoint="highly_rated" />
        {/* <ContentSlider title="Trending" endpoint="trending" /> */}
        <ContentSlider title="Rated By You" endpoint="ratings" />
        <ContentSlider title="Action Movies" />
        <ContentSlider title="Adventure Movies" />
        <ContentSlider title="War Movies" />
        <ContentSlider title="Fantasy Movies" />
        <ContentSlider title="Horror Movies" />
        <ContentSlider title="Documentary Movies" />
        <ContentSlider title="Mystery Movies" />
        <ContentSlider title="Drama Movies" />
        <ContentSlider title="Kids' Movies" />
        <ContentSlider title="Romance Movies" />
        <ContentSlider title="IMAX Movies" />
        <ContentSlider title="Comedy Movies" />
        <ContentSlider title="Western Movies" />
        <ContentSlider title="Animation Movies" />
        <ContentSlider title="Crime Movies" />
        <ContentSlider title="Musical Movies" />
        <ContentSlider title="Thriller Movies" />
        <ContentSlider title="Sci-Fi Movies" />
        <ContentSlider title="Film Noir Movies" />
    </>)
}
export default Dashboard;