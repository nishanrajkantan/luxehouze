import "./watchtable.scss";
import { Link } from "react-router-dom";
import React, { useState, useEffect } from 'react'
import Box from '@mui/material/Box';
import { DataGrid } from '@mui/x-data-grid'
import axios from 'axios';

const watchColumns = [
  { field: "id", headerName: "ID", width: 70 },
  {
    field: "brand",
    headerName: "Brand",
    width: 230,
    // renderCell: (params) => {
    //   return (
    //     <div className="cellWithImg">
    //       <img className="cellImg" src={params.row.img} alt="avatar" />
    //       {params.row.brand}
    //     </div>
    //   );
    // },
    headerClassName: 'super-app-theme--header',
  },
  {
    field: "model_name",
    headerName: "Model",
    width: 230,
    headerClassName: 'super-app-theme--header',
  },

  {
    field: "avg_price",
    headerName: "Average price",
    width: 150,
    headerClassName: 'super-app-theme--header',
  },
  {
    field: "total_listings",
    headerName: "Total Listings",
    width: 150,
    headerClassName: 'super-app-theme--header',
  },
]


function LiveWatches(){

  const actionColumn = [
    {
      field: "action",
      headerName: "Action",
      width: 200,
      renderCell: (params) => {
        return (
          <div className="cellAction">
            <Link to="/users/test" style={{ textDecoration: "none" }}>
              <div className="viewButton">View</div>
            </Link>
            <div
              className="deleteButton"
              onClick={() => handleDelete(params.row.id)}
            >
              Delete
            </div>
          </div>
        );
      },
    },
  ];

const [watchRows, setTableData] = useState([])

useEffect(() => {
    const interval = setInterval(() => {
      axios
        .get(
          'http://instabi.datamicron.com:8235/get_all_watch_info',
          { crossDomain: true })
        .then(res => {            
            setTableData(res.data);
          console.log(res.data);
        })
        .catch(error => console.log(error));
    }, 500);
  }, []);

console.log(watchRows)

const handleDelete = (id) => {
  setTableData(watchRows.filter((item) => item.id !== id));
};

  return (
    <div className="watchtable">
      <div className="watchtableTitle">
        Watches
        <Link to="/users/new" className="link">
          Add New
        </Link>
      </div>
      <Box
            sx={{
              height: 530,
              width: '100%',
              '& .super-app-theme--header': {backgroundColor: 'rgb(175, 206, 71, 0.5)',
              },
            }}
      >
        <DataGrid
          className="datagrid"
          rows={watchRows}
          columns={watchColumns.concat(actionColumn)}
          pageSize={20}
          rowsPerPageOptions={[20]}
          // checkboxSelection
        />
      </Box>
    </div>
  );

}

export default LiveWatches;