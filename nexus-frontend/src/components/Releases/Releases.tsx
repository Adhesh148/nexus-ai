import * as React from 'react';
import AddIcon from '@mui/icons-material/Add';

import './Releases.scss'
import TemplateCard from './TemplateCard';
import { SimpleEditor } from '../SimpleEditor/SimpleEditor';
import { Backdrop, Button, CircularProgress, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from '@mui/material';
import ReleaseDialog from './ReleaseDialog';
import { useReleaseStore } from '../../stores/releaseStore';

export default function Releases() {

    const [release, setRelease] = React.useState('');
    const [template, setTemplate] = React.useState('');
    const [title, setTitle] = React.useState('');
    const [dialogContent, setDialogContent] = React.useState('');
    const [openDialog, setOpenDialog] = React.useState(false);
    const [isNewDialog, setIsNewDialog] = React.useState(false);

    const getReleases = useReleaseStore((state) => state.getReleases);
    const getTemplates = useReleaseStore((state) => state.getTemplates);
    const releases = useReleaseStore((state) => state.releases);
    const templates = useReleaseStore((state) => state.templates);
    const loading = useReleaseStore((state) => state.loading);
    
    const generateReleaseNote = useReleaseStore((state) => state.generateReleaseNote);
    const generatedReleaseNote = useReleaseStore((state) => state.generatedReleaseNote);

    React.useEffect(() => {
        const loadReleases = async () => {
            await getReleases();
        }

        const loadTemplates = async () => {
            await getTemplates();
        }

        loadReleases();
        loadTemplates();
    }, [getReleases, getTemplates]);

    React.useEffect(() => {
        console.log("Generated Release Note:", generatedReleaseNote);
      }, [generatedReleaseNote]);
    

    const handleReleaseChange = (event: SelectChangeEvent) => {
        setRelease(event.target.value as string);
    };

    const handleTemplateChange = (event: SelectChangeEvent) => {
        setTemplate(event.target.value as string);
    };

    const handleClick = (template: string, template_name: string, isNew: boolean = false) => {
        setIsNewDialog(isNew);
        setDialogContent(template);
        setTitle(template_name);
        console.log("dialog opened ", template)
        setOpenDialog(true);
    }

    const handleGenerateClick = async () => {
        console.log("template selected ", template)
        console.log("release selected ", release)

        await generateReleaseNote(release, template); 
    }

    return (
        <div className="release-div">
            <Backdrop
                sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                open={loading}
            >
                <CircularProgress color="inherit" />
            </Backdrop>
            <div className="release-template-div">
                <div className="release-template-new-div" onClick={() => handleClick("", "", true)}>
                    <div className="release-template-new-div-pseudo"><AddIcon fontSize='large' /></div>
                </div>

                <div className="release-cards-div">
                    {
                        templates.map((template) => (
                            <TemplateCard key={template.template_id} onClick={() => handleClick(template.template_content, template.template_name)} template={template} />
                        ))
                    }
                    <ReleaseDialog 
                        openDialog={openDialog} 
                        setOpenDialog={setOpenDialog} 
                        content={dialogContent} 
                        setContent={setDialogContent} 
                        isNew={isNewDialog} 
                        title={title}
                    />
                </div>
            </div>
            
            <div className="release-table-div">
                <div className="release-editor-actions">
                    <div className="release-editor-actions-select">
                        <FormControl sx={{ width: 250, marginRight: '50px' }}>
                            <InputLabel id="release-select-label">Release</InputLabel>
                            <Select
                                labelId="release-select-label"
                                id="release-select"
                                value={release}
                                label="Release"
                                onChange={handleReleaseChange}
                            >
                                {
                                    releases.map((release, indx) => (
                                        <MenuItem key={release.release_id} value={release.release_name}>{release.release_name}</MenuItem>
                                    ))
                                }
                            </Select>
                        </FormControl>
                        <FormControl sx={{ width: 250, marginRight: '50px' }}>
                            <InputLabel id="template-select-label">Template</InputLabel>
                            <Select
                                labelId="template-select-label"
                                id="template-select"
                                value={template}
                                label="Template"
                                onChange={handleTemplateChange}
                            >
                                {
                                    templates.map((template) => (
                                        <MenuItem key={template.template_id} value={template.template_id}>{template.template_name}</MenuItem>
                                    ))
                                }
                            </Select>
                        </FormControl>
                    </div>
                    <div className="release-editor-actions-button">
                        <Button component="label" variant="contained" sx={{ borderRadius: 28, minWidth: '130px', minHeight: '45px' }} onClick={handleGenerateClick}>
                            <AddIcon />
                            <span className="stories-header-button-label">Generate Release Note</span>
                        </Button>
                    </div>
                </div>
                <div className="release-editor-div">
                    <SimpleEditor key={generatedReleaseNote} content={generatedReleaseNote} />
                </div>

            </div>
        </div>
    )
}