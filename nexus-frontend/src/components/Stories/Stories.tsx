import { Backdrop, Box, Button, CircularProgress, Tab, Tabs } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import * as React from 'react';

import './Stories.scss';
import StageTable from './StageTable';
import CreatedTable from './CreatedTable';
import StorySelectionDialog from './StoryDialog';
import { useKnowledgeStore } from '../../stores/knowledgeStore';
import { useIssueStore } from '../../stores/issueStore';

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

function CustomTabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;
  
    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
      </div>
    );
  }

function a11yProps(index: number) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
}

export default function Stories() {
    const [value, setValue] = React.useState(0);
    const [openDialog, setOpenDialog] = React.useState(false);
    const getArticles = useKnowledgeStore((state) => state.getArticles);
    const loading = useIssueStore((state) => state.loading);
    const getIssues = useIssueStore((state) => state.getIssues);

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };

    const handleClick = () => {
        setOpenDialog(true);
    };

    React.useEffect(() => {
        const loadArticles = async () => {
            await getArticles();
        };

        const loadIssues = async () => {
            await getIssues();
        }

        loadArticles();
        loadIssues();
    }, [getArticles, getIssues]);


    return (
        <div className="stories-div">
            <Backdrop
                sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                open={loading}
            >
                <CircularProgress color="inherit" />
            </Backdrop>
            {/* Header */}
            <div className="stories-header">
                <div className="stories-header-label">
                    Stories & Epics
                </div>
                <div className="stories-header-buttons">
                    <Button component="label" variant="contained" sx={{ borderRadius: 28, minWidth: '130px', minHeight: '45px' }} onClick={handleClick}>
                        <AddIcon />                        
                        <span className="stories-header-button-label">Create Stories</span>
                    </Button>
                </div>
            </div>
            <StorySelectionDialog openDialog={openDialog} setOpenDialog={setOpenDialog} />

            {/* Tables Outer Div */}
            <div className="stories-table-div">

                {/* Tabs */}
                <Box sx={{ width: '100%' }}>
                    <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                        <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                            <Tab label="Staged Stories" {...a11yProps(0)} />
                            <Tab label="Created Stories" {...a11yProps(1)} />
                        </Tabs>
                    </Box>
                    <CustomTabPanel value={value} index={0}>
                        <StageTable/>
                    </CustomTabPanel>
                    <CustomTabPanel value={value} index={1}>
                        <CreatedTable/>
                    </CustomTabPanel>
                </Box>

            </div>
        </div>
    )
}