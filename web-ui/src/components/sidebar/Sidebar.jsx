import "./sidebar.scss";
import DashboardIcon from "@mui/icons-material/Dashboard";
import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import StoreIcon from "@mui/icons-material/Store";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import AccountCircleOutlinedIcon from "@mui/icons-material/AccountCircleOutlined";
import ChatIcon from '@mui/icons-material/Chat';
import WatchIcon from '@mui/icons-material/Watch';
import { Link } from "react-router-dom";
import { DarkModeContext } from "../../context/darkModeContext";
import { useContext } from "react";

const Sidebar = () => {
  const { dispatch } = useContext(DarkModeContext);
  return (
    <div className="sidebar">
      <div className="top">
        <Link to="/" style={{ textDecoration: "none" }}>
          <span className="logo">
          <img id="header-img" src="https://cdn.shopify.com/s/files/1/0566/7982/5558/files/LH-weblogo_190x.png?v=1643212052" 
                 alt="..." 
                 height={13}
              /></span>
        </Link>
      </div>
      {/* <hr height={"0px"}/> */}
      <div className="center">
        <ul>
          <p className="title">MAIN</p>
            <Link to="/" style={{ textDecoration: "none" }}>
              <li>
                <DashboardIcon className="icon" />
                <span>Dashboard</span>
              </li>
            </Link>
          <p className="title">LISTS</p>
          
            <li>
              <PersonOutlineIcon className="icon" />
              <span>My Portfolio</span>
            </li>
          

          <p className="title">INTEREST</p>
          <li>
            <StoreIcon className="icon" />
            <span>Brands</span>
          </li>
          <Link to="/addwatch" style={{ textDecoration: "none" }}>
              <li>
                <WatchIcon className="icon" />
                <span>Watches</span>
              </li>
            </Link>
          <p className="title">SERVICE</p>
            <Link to="/live" style={{ textDecoration: "none" }}>
              <li>
                <ChatIcon className="icon" />
                <span>Live Messages</span>
              </li>
            </Link>
          <p className="title">USER</p>
            <Link to="/users" style={{ textDecoration: "none" }}>
              <li>
                <AccountCircleOutlinedIcon className="icon" />
                <span>Profile</span>
              </li>
            </Link>
          <li>
            <ExitToAppIcon className="icon" />
            <span>Logout</span>
          </li>
        </ul>
      </div>
      <div className="bottom">
        <div
          className="colorOption"
          onClick={() => dispatch({ type: "LIGHT" })}
        ></div>
        <div
          className="colorOption"
          onClick={() => dispatch({ type: "DARK" })}
        ></div>
      </div>
    </div>
  );
};

export default Sidebar;
