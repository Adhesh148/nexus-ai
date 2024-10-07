import { Button } from '@mui/material';
import './Header.scss';
import UserMenu from './UserMenu/UserMenu';
import ProjectMenu from './ProjectMenu/ProjectMenu';
import { useProjectStore } from '../../stores/projectStore';
import ProjectDialog from '../ProjectDialog/ProjectDialog';

const Header: React.FC = () => {

  const toggleNewProjectDialog = useProjectStore((state) => state.toggleNewProjectDialog);
  
  return (
    <header className="header">
      <div className="toolbar">

        {/* logo div with image and brand name */}
        <div className="logo-div">
          <img src={require('../../assets/images/logo_6.png')} alt="Logo" className="logo-img" />
          <span className="logo-name">NexusAI</span>
        </div>

        {/* Menu items */}
        <div className="menu-div">
          <div className="menu-item">
            <ProjectMenu />
          </div>
          <div className="menu-item">
            <Button variant="contained"><span style={{fontSize: '16px', textTransform: 'none'}} onClick={toggleNewProjectDialog}>New Project</span></Button>
            <ProjectDialog />
        </div>
        </div>

        {/* User greeting and menu */}
        <div className="user-div">
          <UserMenu />
        </div>
      </div>
    </header>
  );
};

export default Header;
