import { Box, Divider, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import AddTaskIcon from '@mui/icons-material/AddTask';
import NewReleasesIcon from '@mui/icons-material/NewReleases';
import CodeIcon from '@mui/icons-material/Code';
import SettingsIcon from '@mui/icons-material/Settings';
import { Link, useLocation } from 'react-router-dom';

import './Navbar.scss'

const Navbar: React.FC = () => {

    const location = useLocation(); // Get the current route
    const menuItems = [
        { text: "Chat", path: "/chat", icon: <ChatIcon /> },
        { text: "Knowledge Base", path: "/knowledge-base", icon: <MenuBookIcon /> },
        { text: "Stories & Epics", path: "/stories", icon: <AddTaskIcon /> },
        { text: "Releases", path: "/releases", icon: <NewReleasesIcon /> },
        { text: "My Development", path: "/development", icon: <CodeIcon /> },
    ];

    return (
        <div className="navbar">
            <Box sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper', borderRadius: '15px', height: '100%', position: 'relative' }}>
                <nav aria-label="main mailbox folders">
                    <List>
                        {menuItems.map((item) => (
                            <Link
                                key={item.text}
                                to={item.path}
                                style={{ textDecoration: 'none', color: 'black' }}
                            >
                                <ListItem
                                    disablePadding
                                    selected={location.pathname === item.path}
                                    sx={{
                                        '&.Mui-selected': {
                                            backgroundColor: 'rgba(0, 0, 0, 0.08)',
                                        },
                                    }}
                                >
                                    <ListItemButton>
                                        <ListItemIcon>{item.icon}</ListItemIcon>
                                        <ListItemText primary={item.text} />
                                    </ListItemButton>
                                </ListItem>
                            </Link>
                        ))}
                    </List>
                </nav>
                <div style={{ position: "absolute", bottom: "0", width: "100%" }}>
                    <Divider />
                    <nav aria-label="secondary mailbox folders">
                        <List>
                            <ListItem disablePadding>
                                <ListItemButton>
                                    <ListItemIcon>
                                        <SettingsIcon />
                                    </ListItemIcon>
                                    <ListItemText primary="Settings" />
                                </ListItemButton>
                            </ListItem>
                        </List>
                    </nav>
                </div>

            </Box>
        </div>
    );
}

export default Navbar;