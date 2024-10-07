import { Dialog } from "@mui/material"
import ProjectDialogForm from "./ProjectDialogForm"
import './ProjectDialog.scss'
import { useProjectStore } from "../../stores/projectStore";

const ProjectDialog = () => {
    const newProjectDialogOpen = useProjectStore((state) => state.newProjectDialogOpen);
    const toggleNewProjectDialog = useProjectStore((state) => state.toggleNewProjectDialog);

    return (
        <Dialog open={newProjectDialogOpen} onClose={toggleNewProjectDialog}>
            <ProjectDialogForm handleClose={toggleNewProjectDialog} />
        </Dialog>
    )
}

export default ProjectDialog