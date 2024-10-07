import { IconButton, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Tooltip } from "@mui/material";
import Paper from '@mui/material/Paper';
import { useIssueStore } from "../../stores/issueStore";
import React from "react";
import VisibilityIcon from '@mui/icons-material/Visibility';


export default function CreatedTable () {

    const issues = useIssueStore((state) => state.issues);
    const getIssues = useIssueStore((state) => state.getIssues);

    React.useEffect(() => {
        const loadIssues = async () => {
            await getIssues();
        }

        loadIssues();
    }, [ getIssues]);

    return (
        <div>
            <TableContainer component={Paper} sx={{maxHeight: '500px', overflowY: 'auto'}}>
            <Table sx={{ minWidth: 650, }} aria-label="simple table" stickyHeader>
                <TableHead>
                    <TableRow >
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Issue ID</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Issue Summary</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Issue Description</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Issue Type</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Story Points</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Priority</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {issues.filter((issue) => issue.is_staging === false).map((issue) => (
                        <TableRow
                            key={issue.issue_id}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell><a href={issue.issue_url}>{issue.issue_id}</a></TableCell>
                            <TableCell sx={{ maxWidth: '100px'}}>{issue.summary}</TableCell>
                            <TableCell sx={{ maxWidth: '250px'}}>{issue.description}</TableCell>
                            <TableCell>{issue.issue_type}</TableCell>
                            <TableCell sx={{textAlign: 'left'}}>{issue.story_points}</TableCell>
                            <TableCell>{issue.priority}</TableCell>
                            <TableCell>
                                <Tooltip title="View">
                                    <IconButton aria-label="view">
                                        <VisibilityIcon color="primary" />
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