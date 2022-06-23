import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from '@mui/material';
import Box from '@mui/material/Box';
import './App.css';
import { DataGrid } from '@mui/x-data-grid'

const watchColumns = [
  {
    field: "brand",
    headerName: "Brand",
    headerAlign: 'center',
    width: 130,
    headerClassName: 'super-app-theme--header'
  },
  {
    field: "model_name",
    headerName: "Model",
    headerAlign: 'center',
    width: 100,
    headerClassName: 'super-app-theme--header'
  },

  {
    field: "avg_price",
    headerName: "Average Price (USD)",
    headerAlign: 'center',
    width: 170,
    headerClassName: 'super-app-theme--header'
  },
  {
    field: "watch_price",
    headerName: "Watch Price",
    headerAlign: 'center',
    width: 130,
    headerClassName: 'super-app-theme--header'
  },
  {
    field: "margin_difference",
    headerName: "Margin",
    headerAlign: 'center',
    headerClassName: 'super-app-theme--header',
    align: 'center',
    width: 100,
  },  {
    field: "group_id",
    headerName: "Group ID",
    headerAlign: 'center',
    width: 150,
    headerClassName: 'super-app-theme--header',
    hide:true
  },  {
    field: "sender_name",
    headerName: "Sender Name",
    headerAlign: 'center',
    headerClassName: 'super-app-theme--header',
    width: 150,
  },  {
    field: "message",
    headerName: "Message",
    headerAlign: 'center',
    width: 300,
    headerClassName: 'super-app-theme--header'
  },
  {
    field: "replied",
    headerName: "Replied",
    headerAlign: 'center',
    width: 150,
    hide:true,
    headerClassName: 'super-app-theme--header'
  },
  {
    field: "datetime",
    headerName: "Datetime",
    headerAlign: 'center',
    align: 'center',
    width: 250,
    headerClassName: 'super-app-theme--header'
  },
]


function APITable(){

  const actionColumn = [
    {
      field: "action",
      headerName: "Action",
      width: 235,
      headerAlign: 'center',
      headerClassName: 'super-app-theme--header',
      align:'center',

      renderCell: (params) => {
        return (
          <div className="cellAction" align='center'>

            {/* <div
              className="deleteButton" 
              onClick={() => handleDelete(params.row.id)}
              width= '500'
            >
              Delete
            </div> */}

            <Button variant="contained"  href="#" 
              width= '500'
            >
              Message Dealer
            </Button>
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
        pageSize={10}
        rowsPerPageOptions={[10]}
        // checkboxSelection
      />

      </Box>

    </div>
  );

}

export default APITable;
