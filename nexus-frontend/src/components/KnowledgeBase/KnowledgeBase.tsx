import * as React from 'react';
import './KnowledgeBase.scss'
import { Button, IconButton } from '@mui/material';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import SearchIcon from '@mui/icons-material/Search';
import KnowledgeTable from './KnowledgeTable';
import { styled } from '@mui/material/styles';
import { useKnowledgeStore } from '../../stores/knowledgeStore';
import { ArticleType } from '../../types/KnowledgeType';
import { useProjectStore } from '../../stores/projectStore';

const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
  });

export default function KnowledgeBase() {
    const [searchInput, setSearchInput] = React.useState("");
    const [filteredArticles, setFilteredArticles] = React.useState<ArticleType[]>([]);

    const uploadFiles = useKnowledgeStore((state) => state.addArticles);
    const getArticles = useKnowledgeStore((state) => state.getArticles);
    const articles = useKnowledgeStore((state) => state.articles);
    const projectId = useProjectStore((state) => state.currentProjectId);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchInput(e.target.value);
    };

    React.useEffect(() => {
        const loadArticles = async () => {
            await getArticles();
        };

        loadArticles();
    }, [getArticles, projectId]);

    React.useEffect(() => {
        setFilteredArticles(
            articles.filter((article) =>
                article.article_name.toLowerCase().includes(searchInput.toLowerCase())
            )
        );
    }, [searchInput, articles]);

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            const files: File[] | null = Array.from(event.target.files);
            uploadFiles(files)
            console.log("Uploaded file(s): ", files);

            // Reset the file input after processing
            event.target.value = '';
        }   
    }

    return (
        <div className="knowledge-div">
            {/* Header */}
            <div className="knowledge-header">
                <div className="knowledge-header-label">
                    Knowledge Base
                </div>
                <div className="knowledge-header-buttons">
                    <Button component="label" variant="contained" sx={ { borderRadius: 28,  minWidth: '130px', minHeight: '45px' } }>
                        <ArrowUpwardIcon />
                        <span className="knowledge-header-button-label">Upload</span> 
                        <VisuallyHiddenInput type="file" onChange={handleFileUpload}/>
                    </Button>
                </div>
            </div>

            {/* Table */}
            <div className="knowledge-table-div">

                {/* Table Search Bar */}
                <div className="knowledge-table-search-div">
                    <div className="search-input-wrapper">
                        <input
                            type="text"
                            className="search-input-field"
                            value={searchInput}
                            onChange={handleInputChange}
                            placeholder="Search..."
                        />
                        <IconButton aria-label="search" type="submit">
                            <SearchIcon sx={{ fontSize: 30 }} />
                        </IconButton>
                    </div>
                </div>

                {/* Table */}
                <div className="knowledge-table">
                    <KnowledgeTable articles={filteredArticles}/>
                </div>
            </div>
        </div>
    )
}