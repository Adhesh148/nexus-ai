import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {
    CircularProgress,
    circularProgressClasses,
    IconButton,
    Tooltip
} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete';
import DownloadIcon from '@mui/icons-material/Download';
import { red } from '@mui/material/colors';
import { ArticleType } from '../../types/KnowledgeType';
import { useKnowledgeStore } from '../../stores/knowledgeStore';
import DoneIcon from '@mui/icons-material/Done';

export interface Props {
    articles: ArticleType[]
}

export default function KnowledgeTable(props: Props) {

    const deleteArticle = useKnowledgeStore((state) => state.deleteArticle);
    const downloadArticle = useKnowledgeStore((state) => state.downloadArticle);

    const handleDeleteClick = (article_id: string) => {
        deleteArticle(article_id);
    };

    const handleDownloadClick = (article_id: string) => {
        downloadArticle(article_id);
    };

    return (
        <TableContainer component={Paper} sx={{maxHeight: '500px', overflowY: 'auto'}}>
            <Table sx={{ minWidth: 650, }} aria-label="simple table" stickyHeader>
                <TableHead>
                    <TableRow >
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>File Name</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>File Type</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Timestamp</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Processing Status</TableCell>
                        <TableCell sx={{ backgroundColor: "#f1f1f1", fontWeight: "700" }}>Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {props.articles.map((article) => (
                        <TableRow
                            key={article.article_id}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell>{article.article_name}</TableCell>
                            <TableCell>{article.article_type}</TableCell>
                            <TableCell>{article.timestamp}</TableCell>
                            <TableCell sx={{textAlign: 'left'}}>
                            {!article.is_processing ? (
                                <DoneIcon sx={{marginLeft: '50px'}}/>
                            ) : (
                                <CircularProgress
                                    variant="indeterminate"
                                    disableShrink
                                    sx={{
                                        color: (theme) => (theme.palette.mode === 'light' ? '#1a90ff' : '#308fe8'),
                                        animationDuration: '550ms',
                                          position: 'relative',
                                          left: 50,
                                          top: 0,
                                        [`& .${circularProgressClasses.circle}`]: {
                                            strokeLinecap: 'round',
                                        },
                                    }}
                                    size={20}
                                    thickness={4}
                                    {...props}
                                />
                            )}
                            </TableCell>
                            <TableCell>
                                <Tooltip title="Download">
                                    <IconButton aria-label="download" onClick={() => handleDownloadClick(article.article_id)}>
                                        <DownloadIcon color="primary" />
                                    </IconButton>
                                </Tooltip>
                                <Tooltip title="Delete">
                                    <IconButton aria-label="delete" sx={{ marginLeft: '10px' }} onClick={() => handleDeleteClick(article.article_id)}>
                                        <DeleteIcon sx={{ color: red[600] }} />
                                    </IconButton>
                                </Tooltip>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}