import "./table.scss";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import Button from '@mui/material/Button';


const List = () => {
  const rows = [
    {
      model: "Royal Oak",
      lastprice: 1456.11,
      link: "https://cdn.shopify.com/s/files/1/0566/7982/5558/products/1200x1600_25839ST_360x.png",
      change: +0.51,
      percentchange: +0.22,
      volume: 22,
      avgvolume: 44,
      marketcap: 9658,
      action: "Message Dealer",
    },
    {
      model: "Royal Oak Jumbo",
      lastprice: 27.38,
      link: "https://cdn.shopify.com/s/files/1/0566/7982/5558/products/Luxehouze_9_360x.png",
      change: +0.42,
      percentchange: +0.33,
      volume: 12,
      avgvolume: 24,
      marketcap: 12311,
      action: "Message Dealer",
    },
    {
      model: "Royal Oak Double",
      lastprice: 453.23,
      link: "https://cdn.thewatchpages.com/app/uploads/2019/05/13221955/audemars-piguet-royal-oak-double-balance-wheel-openworked-15467oroo1256or01-800x1315.jpg",
      change: +0.27,
      percentchange: +0.62,
      volume: 52,
      avgvolume: 104,
      marketcap: 41211,
      action: "Message Dealer",
    },
    {
      model: "Nautilus",
      lastprice: 39.45,
      link: "https://cdn.shopify.com/s/files/1/0566/7982/5558/products/image_2264f619-52e4-4b95-b149-0f5136c195be_360x.png",
      change: -0.38,
      percentchange: -0.12,
      volume: 35,
      avgvolume: 70,
      marketcap: 4223,
      action: "Message Dealer",
    },
    {
      model: "Aquanaut",
      lastprice: 58.94,
      link: "https://cdn.shopify.com/s/files/1/0566/7982/5558/products/5269200RLH_360x.png",
      change: -0.65,
      percentchange: -0.78,
      volume: 24,
      avgvolume: 48,
      marketcap: 65955,
      action: "Message Dealer",
    },
  ];
  return (
    <TableContainer component={Paper} className="table">
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell className="tableCell" style={{fontWeight: '700'}}>Models</TableCell>
            <TableCell className="tableCell" style={{fontWeight: '700'}}>Last Price</TableCell>
            <TableCell className="tableCell" style={{fontWeight: '700'}}>Change</TableCell>
            <TableCell className="tableCell" style={{fontWeight: '700'}}>%Change</TableCell>
            <TableCell className="tableCell" style={{fontWeight: '700'}}>Volume</TableCell>
            <TableCell className="tableCell" style={{fontWeight: '700'}}>Avg. Volume</TableCell>
            <TableCell className="tableCell" style={{fontWeight: '700'}}>Market Cap</TableCell>
            <TableCell className="tableCell" style={{fontWeight: '700'}}>Action</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.model}>
              <TableCell className="tableCell"><a href={row.link}>{row.model}</a></TableCell>
              <TableCell className="tableCell">{row.lastprice}</TableCell>
              <TableCell className="tableCell">{row.change}</TableCell>
              <TableCell className="tableCell">
              {(() => {
                if (row.percentchange > 0) {
                  return (
                    <div className="change positive">
                      {row.percentchange}%
                    </div>
                  )
                } else {
                  return (
                    <div className="change negative">
                      {row.percentchange}%
                    </div>
                  )
                }
                })()}
              </TableCell>
              <TableCell className="tableCell">{row.volume}</TableCell>
              <TableCell className="tableCell">{row.avgvolume}</TableCell>
              <TableCell className="tableCell">{row.marketcap}</TableCell>
              <TableCell className="tableCell"><Button variant="contained" color="inherit">{row.action}</Button></TableCell>  
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default List;
