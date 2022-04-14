import "./widget.scss";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import AccountBalanceWalletOutlinedIcon from "@mui/icons-material/AccountBalanceWalletOutlined";
import ShoppingCartOutlinedIcon from "@mui/icons-material/ShoppingCartOutlined";
import MonetizationOnOutlinedIcon from "@mui/icons-material/MonetizationOnOutlined";

const Widget = ({ type }) => {
  let data;

  //temporary
  // const amount = 100;
  // const diff = 20;

  switch (type) {
    case "model1":
      data = {
        title: "Royal Oak",
        isMoney: true,
        link: "See all users",
        amount:2155.45,
        icon: (
          <PersonOutlinedIcon
            className="icon"
            style={{
              color: "crimson",
              backgroundColor: "rgba(255, 0, 0, 0.2)",
            }}
          />
        ),
        percentage: +11.39,
        percentageicon: <KeyboardArrowUpIcon />
      };
      break;
    case "model2":
      data = {
        title: "Nautilus",
        isMoney: true,
        link: "View all orders",
        amount:2455.35,
        icon: (
          <ShoppingCartOutlinedIcon
            className="icon"
            style={{
              backgroundColor: "rgba(218, 165, 32, 0.2)",
              color: "goldenrod",
            }}
          />
        ),
        percentage: +1.39,
        percentageicon: <KeyboardArrowUpIcon />
      };
      break;
    case "model3":
      data = {
        title: "Aquanaut",
        isMoney: true,
        link: "View net earnings",
        amount:6355.45,
        icon: (
          <MonetizationOnOutlinedIcon
            className="icon"
            style={{ backgroundColor: "rgba(0, 128, 0, 0.2)", color: "green" }}
          />
        ),
        percentage: -7.39,
        percentageicon: <KeyboardArrowUpIcon />
      };
      break;
    case "model4":
      data = {
        title: "Royal Oak Jumbo",
        isMoney: true,
        link: "See details",
        amount:1155.45,
        icon: (
          <AccountBalanceWalletOutlinedIcon
            className="icon"
            style={{
              backgroundColor: "rgba(128, 0, 128, 0.2)",
              color: "purple",
            }}
          />
        ),
        percentage: -8.58,
        percentageicon: <KeyboardArrowDownIcon />
      };
      break;
    case "model5":
      data = {
        title: "Royal Oak Double",
        isMoney: true,
        link: "See details",
        amount:61.29,
        icon: (
          <AccountBalanceWalletOutlinedIcon
            className="icon"
            style={{
              backgroundColor: "rgba(128, 0, 128, 0.2)",
              color: "purple",
            }}
          />
        ),
        percentage: -5.58,
        percentageicon: <KeyboardArrowDownIcon />
      };
      break;
    case "model6":
      data = {
        title: "Royal Oak Double",
        isMoney: true,
        link: "See details",
        amount:1908.67,
        icon: (
          <AccountBalanceWalletOutlinedIcon
            className="icon"
            style={{
              backgroundColor: "rgba(128, 0, 128, 0.2)",
              color: "purple",
            }}
          />
        ),
        percentage: -5.58,
        percentageicon: <KeyboardArrowDownIcon />
      };
      break;
    case "model7":
      data = {
        title: "Royal Oak Double",
        isMoney: true,
        link: "See details",
        amount:2764.98,
        icon: (
          <AccountBalanceWalletOutlinedIcon
            className="icon"
            style={{
              backgroundColor: "rgba(128, 0, 128, 0.2)",
              color: "purple",
            }}
          />
        ),
        percentage: -5.58,
        percentageicon: <KeyboardArrowDownIcon />
      };
      break;
    default:
      break;
  }

  return (
    <div className="widget">
      <div className="left">
        <span className="title">{data.title}</span>
        <span className="counter">
          {data.isMoney && "$"} {data.amount}
        </span>
        {/* <span className="link">{data.link}</span> */}
      </div>
      <div className="right">
        {(() => {
        if (data.percentage > 0) {
          return (
            <div className="percentage positive">
              {<KeyboardArrowUpIcon />}
              {data.percentage} %
            </div>
          )
        } else {
          return (
            <div className="percentage negative">
              {<KeyboardArrowDownIcon />}
              {data.percentage}%
            </div>
          )
        }
        })()}
      </div>
    </div>
  );
};

export default Widget;
