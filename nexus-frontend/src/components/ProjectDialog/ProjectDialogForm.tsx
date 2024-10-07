import { Button, styled, TextField } from "@mui/material";
import React, { useState } from "react";
import CodeIcon from '@mui/icons-material/Code';
import ArticleIcon from '@mui/icons-material/Article';
import WorkHistoryIcon from '@mui/icons-material/WorkHistory';

import './ProjectDialogForm.scss'
import { ConfluenceConfig, GithubConfig, JiraConfig, ProjectConfig } from "../../types/ProjectType";
import { isConfluenceConfig, isGithubConfig, isJiraConfig, parseAndValidateConfig } from "../../utils/utils";
import { useProjectStore } from "../../stores/projectStore";

const StyledTextField = styled(TextField)(({ theme }) => ({
    margin: "1rem",
    width: "400px",
}));

const ProjectDialogForm = (props: { handleClose: () => void }) => {
    const [projectName, setProjectName] = useState("");
    const [projectDesc, setProjectDesc] = useState("");
    const [githubConfig, setGithubConfig] = useState("");
    const [confluenceConfig, setConfluenceConfig] = useState("");
    const [jiraConfig, setJiraConfig] = useState("");

    const createProject = useProjectStore((state) => state.addProject); 

    const handleSubmit = async (e: React.SyntheticEvent) => {
        e.preventDefault();
        console.log(projectName);

        // parse configs
        const parsedJiraConfig = parseAndValidateConfig<JiraConfig>(jiraConfig, isJiraConfig);
        const parsedConfluenceConfig = parseAndValidateConfig<ConfluenceConfig>(confluenceConfig, isConfluenceConfig);
        const parsedGithubConfig = parseAndValidateConfig<GithubConfig>(githubConfig, isGithubConfig);
        const projectConfig: ProjectConfig = {
            jira: parsedJiraConfig,
            github: parsedGithubConfig,
            confluence: parsedConfluenceConfig
        }
        await createProject(projectName, projectDesc, projectConfig);

        props.handleClose();

    };

    return (
        <form
            onSubmit={handleSubmit}
            style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                width: '500px',
                padding: "2rem",
            }}
        >

            <div className="form-header" style={{ marginLeft: '15px', fontSize: ' 18px', fontWeight: '800' }}>
                Create New Project
            </div>
            <StyledTextField
                label="Project Name"
                variant="filled"
                required
                value={projectName}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setProjectName(e.target.value)
                }
            />
            <StyledTextField
                label="Project Description"
                variant="filled"
                value={projectDesc}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setProjectDesc(e.target.value)
                }
            />

            <div className="form-setup-section" style={{ display: 'flex', flexDirection: 'column' }}>
                <div className="form-setup-section-header" style={{ display: 'flex', flexDirection: 'column', marginLeft: '15px', marginTop: '10px' }}>
                    <span style={{ fontSize: '16px', fontWeight: '600' }}>Project Setup</span>
                    <span style={{ fontSize: '14px' }}>Setup your project by connecting with your project tools</span>
                </div>


                <div className="form-field-with-icon">
                    <CodeIcon />
                    <StyledTextField
                        label="Github Configuration"
                        variant="filled"
                        value={githubConfig}
                        multiline
                        rows={3}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                            setGithubConfig(e.target.value)
                        }
                    />
                </div>

                <div className="form-field-with-icon">
                    <WorkHistoryIcon />
                    <StyledTextField
                        label="JIRA Configuration"
                        variant="filled"
                        value={jiraConfig}
                        multiline
                        rows={3}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                            setJiraConfig(e.target.value)
                        }
                    />
                </div>

                <div className="form-field-with-icon">
                    <ArticleIcon />
                    <StyledTextField
                        label="Confluence Configuration"
                        variant="filled"
                        value={confluenceConfig}
                        multiline
                        rows={3}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                            setConfluenceConfig(e.target.value)
                        }
                    />
                </div>

            </div>

            <div>
                <Button onClick={props.handleClose} color="error">Cancel</Button>
                <Button
                    variant="contained"
                    color="primary"
                    type="submit"
                    sx={{ margin: "2rem" }}
                >
                    Create
                </Button>
            </div>
        </form>
    );
};

export default ProjectDialogForm;