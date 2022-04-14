import "./featured.scss";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import { Doughnut } from "react-chartjs-2";
import 'chart.js/auto'
import {Chart, PointElement} from 'chart.js';
Chart.register(PointElement);

const Featured4 = () => {
  const data = {
    labels: [
      'Patek Philippe',
      'Audemars Piquet',
      'Richard Mille',
      'Rolex',
    ],
    datasets: [{
      label: 'My First Dataset',
      data: [300, 200, 100, 40],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(255, 86, 224)'
      ],
      hoverOffset: 4
    }]
  }

  const options = {
    plugins: {
      legend: {
        display: true,
        position:'right',
        maxWidth: 150
      }
    },
    maintainAspectRatio: false
  };

  return (
    <div className="featured">
      <div className="top">
        <h1 className="title">Deals Diversity</h1>
        <MoreVertIcon fontSize="small" />
      </div>
      <div className="bottom">
        <div className="featuredChart">
          <div className="donut">
            <Doughnut data={data} options={options} width={"110%"} height={"110%"}/>
          </div>
        </div>
      </div>
    </div>
    
  );
};

export default Featured4;
