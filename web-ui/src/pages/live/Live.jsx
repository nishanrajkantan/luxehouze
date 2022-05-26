import "./live.scss"
import Sidebar from "../../components/sidebar/Sidebar"
import Navbar from "../../components/navbar/Navbar"
import Datatable from "../../components/datatable/Datatable"
import Live_Table from "../../components/live-table/Live-Table"
import DataGrid1 from "../../components/live-table/DataGrid"

const Live = () => {
  return (
    <div className="list">
      <Sidebar/>
      <div className="listContainer">
        <Navbar/>
        {/* <Live_Table/> */}
        <DataGrid1/>
      </div>
    </div>
  )
}

export default Live