import "./featured.scss";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import "react-circular-progressbar/dist/styles.css";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

const Featured1 = () => {
  let totaldeals = 74520.88;
  let deals = 10.56;
  let prevdeals = 74520.88;
  let percentage = 0.12;

  return (
    <div className="featured">
      <div className="top">
        <h1 className="title">Total Deals</h1>
        <MoreVertIcon fontSize="small" />
      </div>
      <div className="bottom">
          {/* <CircularProgressbar value={70} text={"70%"} strokeWidth={5} /> */}
        <h1 className="h2"><strong>${totaldeals}</strong></h1>
        
        <div className="desc"> 
          <div className="left">Previous Deals :</div>
          <div className="right">${prevdeals}</div>
        </div> 
        <div className="desc">
          <div className="left">Daily Deals :</div>
          <div className="right">${deals}</div>
        </div>
        <div className="desc">
          <div className="left">Daily Difference :</div>
          <div className="right">
            {(() => {
              if (percentage > 0) {
                return (
                  <div className="percentage positive">
                    {<KeyboardArrowUpIcon />}
                    {percentage} %
                  </div>
                )
              } else {
                return (
                  <div className="percentage negative">
                    {<KeyboardArrowDownIcon />}
                    {percentage}%
                  </div>
                )
              }
              })()}
          </div>
        </div>
      </div>
    </div>
    
  );
};

export default Featured1;
