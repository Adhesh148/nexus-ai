import * as React from 'react';
import { IconButton, ListItemIcon, Menu, MenuItem } from '@mui/material';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import DriveFileRenameOutlineIcon from '@mui/icons-material/DriveFileRenameOutline';
import DeleteIcon from '@mui/icons-material/Delete';
import DownloadIcon from '@mui/icons-material/Download';
import StarIcon from '@mui/icons-material/Star';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';

import './ChatHistoryLabel.scss'
import { ChatSession } from '../../../types/MessageType';

interface ChatHistoryLabelProps {
    session: ChatSession;
}

export default function ChatHistoryLabel({ session }: ChatHistoryLabelProps) {
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

    const open = Boolean(anchorEl);
    const handleClick = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <div className="chat-history-label">
            <div className="chat-history-label-text">
                <p>{session.session_name}</p>
                
            </div>
            <div className="chat-history-label-menu">
            <IconButton
                onClick={handleClick}
                size="small"
                sx={{ ml: 4 }}
                aria-controls={open ? 'chat-history-menu' : undefined}
                aria-haspopup="true"
                aria-expanded={open ? 'true' : undefined}
            >
                <MoreHorizIcon sx={{fontSize: '20px'}} />
            </IconButton>
            <Menu
                id="long-menu"
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                PaperProps={{
                    elevation: 0,
                    sx: {
                        overflow: 'visible',
                        filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                        mt: 1.5,
                        '& .MuiAvatar-root': {
                            width: 32,
                            height: 32,
                            ml: -0.5,
                            mr: 1,
                        },
                        '&::before': {
                            content: '""',
                            display: 'block',
                            position: 'absolute',
                            top: 0,
                            right: 14,
                            width: 10,
                            height: 10,
                            bgcolor: 'background.paper',
                            transform: 'translateY(-50%) rotate(45deg)',
                            zIndex: 0,
                        },
                    },
                }}
            >
                <MenuItem onClick={handleClose}>
                    <ListItemIcon>
                        <DriveFileRenameOutlineIcon fontSize="small" />
                    </ListItemIcon>
                    Rename
                </MenuItem>
                <MenuItem onClick={handleClose}>
                    <ListItemIcon>
                        <StarIcon fontSize="small" />
                    </ListItemIcon>
                    Favorite
                </MenuItem>
                <MenuItem onClick={handleClose}>
                    <ListItemIcon>
                        <ContentCopyIcon fontSize="small" />
                    </ListItemIcon>
                    Duplicate
                </MenuItem>
                <MenuItem onClick={handleClose}>
                    <ListItemIcon>
                        <DownloadIcon fontSize="small" />
                    </ListItemIcon>
                    Download
                </MenuItem>
                <MenuItem onClick={handleClose} sx={{color: "red"}}>
                    <ListItemIcon>
                        <DeleteIcon fontSize="small" />
                    </ListItemIcon>
                    Delete Chat
                </MenuItem>
            </Menu>
            </div>
        </div>
    );
}