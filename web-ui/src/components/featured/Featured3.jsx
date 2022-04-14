import "./featured.scss";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import "react-circular-progressbar/dist/styles.css";
import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto'
import {Chart, PointElement} from 'chart.js';
Chart.register(PointElement);

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);


const Featured3 = () => {

  const options = {
    indexAxis: 'y',
    elements: {
      bar: {
        borderWidth: 2,
      },
    },
    responsive: true,
    plugins: {
      legend: {
        display:false,
        position: 'right',
        maxWidth: 150
      },
      title: {
        display: false,
        text: 'Chart.js Horizontal Bar Chart',
      },
    scales: {
      x: {
        grid: {
          display: false,
          drawBorder: false,
        },
      },
      y: {
        grid: {
          display:false,
          drawBorder: false,
          },
        },
      },
    },
    maintainAspectRatio: false
  };

  const labels = ['Audemars Piquet', 'Richard Mille', 'Patek Philippe', 'Rolex'];

  const data = {
    labels,
    datasets: [
      {
        label: 'Dataset 1',
        data: [900,700,500,300],
        borderColor: 'transparent',
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)',
          'rgb(255, 86, 224)',
        ],
        hoverOffset: 4
      },
    ],
  };
  
  return (
    <div className="featured">
      <div className="top">
        <h1 className="title">Deals Valuation</h1>
        <MoreVertIcon fontSize="small" />
      </div>
      <div className="bottom">
        <div className="featuredChart">
          <div className="bar">
            <Bar options={options} data={data} width={"50%"} height={"120%"}/>
          </div>
        </div>
      </div>
    </div>
    
  );
};

export default Featured3;
