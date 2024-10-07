import * as React from 'react';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { useProjectStore } from '../../../stores/projectStore';
import { Project } from '../../../types/ProjectType';

export default function ProjectMenu() {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const projects: Project[]  = useProjectStore(state => state.projects);
  const toggleProject = useProjectStore(state => state.toggleCurrentProject);
  const [selectedIndex, setSelectedIndex] = React.useState(0);

  const open = Boolean(anchorEl);

  React.useEffect(() => {
    if (projects.length > 0) {
      toggleProject(projects[selectedIndex].project_id);
    }
  }, [selectedIndex, projects, toggleProject]);
  
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  
  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleMenuItemClick = (
    event: React.MouseEvent<HTMLElement>,
    index: number,
    newProjectId: string
  ) => {
    setSelectedIndex(index);
    setAnchorEl(null);
  };

  return (
    <div>
      <Button
        id="basic-button"
        aria-controls={open ? 'basic-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        onClick={handleClick}
      >
        Projects
      </Button>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
        anchorOrigin={{
            vertical: 45,
            horizontal: 0
        }}
      >
        {
          projects.map((project, index) => (
            <MenuItem 
              key={project.project_id} 
              selected={index === selectedIndex}
              onClick={(event) => handleMenuItemClick(event, index, project.project_id)}
              sx={{
                '&.Mui-selected': {
                    backgroundColor: 'rgba(0, 0, 0, 0.08)',
                },
            }}
            >
              {project.project_name}
            </MenuItem>
          ))
        }
      </Menu>
    </div>
  );
}
