import { IconButton, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Tooltip } from "@mui/material";
import Paper from '@mui/material/Paper';
import { useIssueStore } from "../../stores/issueStore";
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import { red, green } from '@mui/material/colors';
import AddIcon from '@mui/icons-material/Add';

export default function StageTable () {

    const deleteIssue = useIssueStore((state) => state.deleteIssue);
    const createIssue = useIssueStore((state) => state.createIssue);
    const issues = useIssueStore((state) => state.issues);

    const handleDeleteClick = (issue_id: string) => {
        deleteIssue(issue_id);
    };

    const handleCreateClick = (issue_id: string) => {
        createIssue(issue_id);
    }

    return (
        <div>
            <TableContainer component={Paper} sx={{maxHeight: '500px', overflowY: 'auto'}}>
            <Table sx={{ minWidth: 650, }} aria-label="simple table" stickyHeader>
                <TableHead>
                    <TableRow >
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Issue Summary</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Issue Description</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Issue Type</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Story Points</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Priority</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {issues.filter((issue) => issue.is_staging === true).map((issue) => (
                        <TableRow
                            key={issue.issue_id}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell sx={{ maxWidth: '100px'}}>{issue.summary}</TableCell>
                            <TableCell sx={{ maxWidth: '250px'}}>{issue.description}</TableCell>
                            <TableCell>{issue.issue_type}</TableCell>
                            <TableCell sx={{textAlign: 'left'}}>{issue.story_points}</TableCell>
                            <TableCell>{issue.priority}</TableCell>
                            <TableCell sx={{textAlign: 'left', marginLeft: '200px'}}>
                                <Tooltip title="View & Edit">
                                    <IconButton aria-label="edit">
                                        <EditIcon color="primary" />
                                    </IconButton>
                                </Tooltip>
                                <Tooltip title="Create Issue">
                                    <IconButton aria-label="confirm" onClick={() => handleCreateClick(issue.issue_id)}>
                                        <AddIcon sx={{ color: green[800] }} color="primary" />
                                    </IconButton>
                                </Tooltip>
                                <Tooltip title="Delete">
                                    <IconButton aria-label="delete" onClick={() => handleDeleteClick(issue.issue_id)}>
                                        <DeleteIcon sx={{ color: red[600] }} />
                                    </IconButton>
                                </Tooltip>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
        </div>
    )
}