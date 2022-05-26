import "./featured.scss";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import { Line } from "react-chartjs-2";
import 'chart.js/auto'
import {Chart, PointElement} from 'chart.js';
Chart.register(PointElement);

const Featured2 = () => {

  const data = {
    labels: ["10/4/22", "11/4/22", "12/4/22", "13/4/22", "14/4/22", "15/4/22"],
    datasets: [
      {
        label: "Purchase",
        data: [33, 53, 85, 41, 44, 65],
        fill: true,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: "rgba(255, 99, 132, 0.2)"
      },
      {
        label: "Deals",
        data: [33, 25, 35, 51, 54, 76],
        fill: true,
        borderColor: "rgba(24, 142, 0, 1)",
        backgroundColor: "rgba(24, 142, 0, 0.2)"
      },
    ]
  };

  const options = {
    plugins: {
      scales: {
        x: {
            ticks: {
                display: false
            }
        },
        y:{
            display: false,
            title: {
              display: true,
              text:'$ Dollar'
            }
        },
      },
      legend: {
        display: true,
      },
    },
  };

  return (
    <div className="featured">
      <div className="top">
        <h1 className="title">Purchasing Trend</h1>
        <MoreVertIcon fontSize="small" />
      </div>
    <div className="bottom">
      <div className="featuredChart"></div>
        <div className="line">
          <Line data={data} options={options} height={80} width={240}/>
        </div>
      </div>
    </div>
  );
}

export default Featured2;
