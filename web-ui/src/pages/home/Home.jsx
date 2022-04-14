import Sidebar from "../../components/sidebar/Sidebar";
import Navbar from "../../components/navbar/Navbar";
import "./home.scss";
import Widget from "../../components/widget/Widget";
import Featured1 from "../../components/featured/Featured1";
import Featured2 from "../../components/featured/Featured2";
import Featured3 from "../../components/featured/Featured3";
import Featured4 from "../../components/featured/Featured4";
import Table from "../../components/table/Table";

const Home = () => {
  return (
    <div className="home">
      <Sidebar />
      <div className="homeContainer">
        <Navbar />
        <div className="widgets">
          <Widget type="model1" />
          <Widget type="model2" />
          <Widget type="model3" />
          <Widget type="model4" />
          <Widget type="model5" />
          {/* <Widget type="model6" /> */}
          {/* <Widget type="model7" /> */}
        </div>
        <div className="charts">
          <Featured1 />
          <Featured2 />
          <Featured3 />
          <Featured4 />
          {/* <Featured5 /> */}
          
        </div>
        {/* <div className="charts">
          <Chart title="Last 6 Months (Revenue)" aspect={2 / 1} />
        </div> */}
        <div className="listContainer">
          <div className="listTitle">Watch Models' Deals</div>
          <Table />
        </div>
      </div>
    </div>
  );
};

export default Home;
