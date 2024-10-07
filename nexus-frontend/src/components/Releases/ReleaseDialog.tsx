import { Button, Dialog, DialogActions, DialogContent, DialogTitle, styled, TextField } from "@mui/material";
import { SimpleEditor } from "../SimpleEditor/SimpleEditor";

import './ReleaseDialog.scss'
import { useState } from "react";
import { useReleaseStore } from "../../stores/releaseStore";

interface Props {
    openDialog: boolean;
    setOpenDialog: React.Dispatch<React.SetStateAction<boolean>>;
    content: string;
    isNew?: boolean;
    setContent:  React.Dispatch<React.SetStateAction<string>>;
    title: string
}

const StyledTextField = styled(TextField)(({ theme }) => ({
    margin: "1rem",
    width: "400px",
}));


export default function ReleaseDialog({ openDialog, setOpenDialog, content, setContent, isNew = false, title}: Props) {

    const [templateName, setTemplateName] = useState<string>(title);
    const createTemplate = useReleaseStore((state) => state.createTemplate);

    const handleClose = () => {
        setOpenDialog(false);
        setTemplateName("")
    };

    const handleSubmit = () => {
        console.log("submitted with name", templateName)
        console.log("submitted with content", content)
        setTemplateName("");
        createTemplate(templateName, content)
        setOpenDialog(false);
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
            fullWidth
        >
            <DialogTitle sx={{ margin: '0px 20px', fontSize: '24px', fontWeight: '600' }}>Template</DialogTitle>
            <DialogContent >
                <div className="release-dialog-content">
                    <StyledTextField
                        label="Template Name"
                        variant="filled"
                        required
                        value={isNew === true ? templateName : title}
                        disabled={isNew === false}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                            setTemplateName(e.target.value)
                        }
                        sx={{width: '500px', margin: 0, marginBottom: '20px'}}
                    />
                    <div className="release-dialog-editor-title">Release Template</div>
                    <div className="release-dialog-editor">
                        <SimpleEditor content={content} setEditorContent={setContent}/>
                    </div>
                </div>

            </DialogContent>
            <DialogActions sx={{ margin: '10px' }}>
                <Button onClick={handleClose} color="error">Cancel</Button>
                {isNew ? (<Button type="submit">Save</Button>) : null}
            </DialogActions>
        </Dialog>
    )
}