import { NavLink } from 'react-router-dom'
import { Menu } from 'antd'
import {
  AppstoreOutlined,
  TeamOutlined,
  LineChartOutlined,
  CalendarOutlined,
  SettingOutlined
} from '@ant-design/icons'


function Navbar() {
  return (
    <Menu mode="horizontal" theme="dark"> 
    <Menu.Item key="dashboard">
       <NavLink to="/"><AppstoreOutlined/>Dashboard</NavLink> 
    </Menu.Item> 
    <Menu.Item key="leads"> 
      <NavLink to="/leads"><TeamOutlined/>Leads</NavLink>
     </Menu.Item> 
     <Menu.Item key="pipeline">
       <NavLink to="/pipeline"><LineChartOutlined/>Pipeline</NavLink> 
     </Menu.Item> 
     <Menu.Item key="followups"> 
      <NavLink to="/followups"><CalendarOutlined/>Follow Ups</NavLink> 
     </Menu.Item>
      <Menu.Item key="settings"> 
        <NavLink to="/settings"><SettingOutlined/>Settings</NavLink> 
     </Menu.Item>
     <button>submit</button>
      </Menu>
  )
}

export default Navbar;

