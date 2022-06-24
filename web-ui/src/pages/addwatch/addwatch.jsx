import "./addwatch.scss"
import Sidebar from "../../components/sidebar/Sidebar"
import Navbar from "../../components/navbar/Navbar"
import LiveWatches from "../../components/datatable/Watchtable"

const Addwatch = () => {
  return (
    <div className="list">
      <Sidebar/>
      <div className="listContainer">
        <Navbar/>
        <LiveWatches/>
      </div>
    </div>
  )
}

export default Addwatch