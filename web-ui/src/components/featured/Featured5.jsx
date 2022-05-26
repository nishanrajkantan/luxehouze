import React, { useState, useEffect } from "react";
 import { Bar, Line } from "react-chartjs-2";
import axios from "axios";

function Featured5() {

  const [data, setData] = useState([]);
  const [posts, setPosts] = useState([]);

  let title = [];
  let id = [];
  useEffect(() => {

    axios.get("https://jsonplaceholder.typicode.com/posts").then(res => {
      const ipl = res.data;
      setPosts(ipl);

      ipl.forEach(record => {
        title.push(record.title);
        id.push(record.id);
      });

      setData({
        Data: {
          labels: title,
          datasets: [
            {
              label: "IPL 2018/2019 Top Run Scorer",
              data: id,
              backgroundColor: [
                "#3cb371",
                "#0000FF",
                "#9966FF",
                "#4C4CFF",
                "#00FFFF",
                "#f990a7",
                "#aad2ed",
                "#FF00FF",
                "Blue",
                "Red"
              ]
            }
          ]
        }
      });
    });
  });

  return (
    <div>
      <Line data={data.Data} />
    </div>
  );
}

export default Featured5;