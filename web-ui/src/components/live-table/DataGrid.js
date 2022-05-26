import React, { useState, useEffect } from 'react'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import Box from '@mui/material/Box';
import axios from 'axios';

const columns = [
  { field: 'message_id', headerName: 'Message ID' , width: 120, headerAlign: 'center', headerClassName: 'super-app-theme--header', hide:true},
  { field: 'timestamp', headerName: 'Timestamp' , width: 110, type: 'dateTime', headerAlign: 'center', headerClassName: 'super-app-theme--header'},
  { field: 'group_id', headerName: 'Group ID' , width: 270, headerAlign: 'center', headerClassName: 'super-app-theme--header'},
  { field: 'sender_id', headerName: 'Sender ID' , width: 293, headerAlign: 'center', headerClassName: 'super-app-theme--header'},
  { field: 'sender_name', headerName: 'Sender Name' , width: 150, headerAlign: 'center', headerClassName: 'super-app-theme--header'},
  { field: 'message', headerName: 'Message' , width: 400, headerAlign: 'center', headerClassName: 'super-app-theme--header'},
  { field: 'image_url', headerName: 'Image URL' , width: 400, headerAlign: 'center', headerClassName: 'super-app-theme--header'}
]

function DataGrid1 () {

  const [tableData, setTableData] = useState([])

    useEffect(() => {
        const interval = setInterval(() => {
          axios
            .get(
              'http://instabi.datamicron.com:8235/latest_message',
              { crossDomain: true })
            .then(res => {            
                setTableData(res.data);
              console.log(res.data);
            })
            .catch(error => console.log(error));
        }, 5000);
      }, []);

  console.log(tableData)


  return (
    <div>
    <div style={{ display: 'flex', height: 110, width: '100%', padding:"10px" }}>
      <Box
      sx={{
        height: 700,
        width: '100%',
        '& .super-app-theme--header': {
          backgroundColor: 'rgba(171,120,78, 0.55)',
        },
      }}
      >
      <DataGrid
        getRowId={(row) => row.message_id}
        rows={tableData}
        columns={columns}
        pageSize={1}
      />
      </Box>
    </div>

    </div>
  )
}

export default DataGrid1