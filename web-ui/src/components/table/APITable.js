import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { DataGrid } from '@mui/x-data-grid'

const watchColumns = [
  {
    field: "brand",
    headerName: "Brand",
    width: 200,
  },
  {
    field: "model_name",
    headerName: "Model",
    width: 150,
  },

  {
    field: "avg_price",
    headerName: "Average price",
    width: 150,
  },
  {
    field: "watch_price",
    headerName: "Watch Price",
    width: 100,
  },
  {
    field: "margin_difference",
    headerName: "Margin",
    width: 100,
  },  {
    field: "group_id",
    headerName: "Group ID",
    width: 150,
  },  {
    field: "sender_name",
    headerName: "Sender Name",
    width: 150,
  },  {
    field: "message",
    headerName: "Message",
    width: 250,
  },
  {
    field: "replied",
    headerName: "Replied",
    width: 150,
  },
  {
    field: "datetime",
    headerName: "Datetime",
    width: 150,
  },
]


function APITable(){

  const actionColumn = [
    {
      field: "action",
      headerName: "Action",
      width: 200,
      renderCell: (params) => {
        return (
          <div className="cellAction">

            <div
              className="deleteButton"
              onClick={() => handleDelete(params.row.id)}
            >
              Reply
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
          'http://instabi.datamicron.com:8235/get_all_deals_info',
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
      <DataGrid
        className="datagrid"
        rows={watchRows}
        columns={watchColumns.concat(actionColumn)}
        pageSize={9}
        rowsPerPageOptions={[9]}
        checkboxSelection
      />
    </div>
  );

}

export default APITable;
