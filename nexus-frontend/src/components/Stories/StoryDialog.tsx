import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { Button, Checkbox, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import { useKnowledgeStore } from '../../stores/knowledgeStore';
import { useIssueStore } from '../../stores/issueStore';

interface StoryDialogProps {
    openDialog: boolean;
    setOpenDialog: React.Dispatch<React.SetStateAction<boolean>>;
}

export default function StorySelectionDialog({ openDialog, setOpenDialog }: StoryDialogProps) {

    const [checked, setChecked] = React.useState<string[]>([]);
    const articles = useKnowledgeStore((state) => state.articles);
    const draftIssues = useIssueStore((state) => state.draftIssues);

    const handleToggle = (value: string) => () => {
        const currentIndex = checked.indexOf(value);
        const newChecked = [...checked];

        if (currentIndex === -1) {
            newChecked.push(value);
        } else {
            newChecked.splice(currentIndex, 1);
        }

        setChecked(newChecked);
    };

    const handleClose = () => {
        setOpenDialog(false);
        setChecked([]);
    };

    const handleSubmit = () => {
        draftIssues(checked)
    }

    return (
            <Dialog
                open={openDialog}
                onClose={handleClose}
                PaperProps={{
                    component: 'form',
                    onSubmit: (event: React.FormEvent<HTMLFormElement>) => {
                        handleSubmit()
                        event.preventDefault();
                        handleClose();
                    },
                }}
            >
                <DialogTitle>Create New Issues</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        To create new issues, select relevant articles from your Knowledge Base. NexusAI will identify
                        business and technical requirements to craft new issues from them.
                    </DialogContentText>

                    <List sx={{ width: '100%', bgcolor: 'background.paper', maxHeight: '400px', overflow: 'auto' }}>
                        {articles.map((article) => {
                            const labelId = `checkbox-list-label-${article.article_id}`;

                            return (
                                <ListItem
                                    key={article.article_id}
                                    disablePadding
                                >
                                    <ListItemButton role={undefined} onClick={handleToggle(article.article_id)} dense>
                                        <ListItemIcon>
                                            <Checkbox
                                                edge="start"
                                                checked={checked.indexOf(article.article_id) !== -1}
                                                tabIndex={-1}
                                                disableRipple
                                                inputProps={{ 'aria-labelledby': labelId }}
                                            />
                                        </ListItemIcon>
                                        <ListItemText id={labelId} primary={`${article.article_name}`} />
                                    </ListItemButton>
                                </ListItem>
                            );
                        })}
                    </List>
                </DialogContent>
                <DialogActions sx={{margin: '10px'}}>
                    <Button onClick={handleClose} color="error">Cancel</Button>
                    <Button type="submit">Create Issues</Button>
                </DialogActions>
            </Dialog>
    );
}
