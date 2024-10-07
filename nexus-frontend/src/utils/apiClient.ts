import { IssueType } from "../types/IssueType"
import { ArticleType } from "../types/KnowledgeType"
import { Project, ProjectConfig } from "../types/ProjectType"
import { ReleaseType, TemplateType } from "../types/TemplateTypes"
import axios from 'axios';

export const API_URL = "http://localhost:8181/nexus/v1"

export type ChatInput = {input: {input: string}}
export type ChatOutput = {
    output: {
        output: string
    }
}

export type FileOutput = {
    file_id: string
    project_id: string
    file_name: string
    file_type: string
    file_path: string
    is_active: boolean
    created_at: string
    artifacts: FileOutput[]
}

// ---------------- APIS for Chat ------------------------------
export const sendChatMessage = async (inputData: ChatInput, sessionId: string, projectId: string): Promise<ChatOutput> => {
    try {
        const response = await fetch(`${API_URL}/chat/invoke?session_id=${sessionId}&project_id=${projectId}`, {
            method: "POST",
            body: JSON.stringify(inputData)
        })

        return response.json();
    } catch (error) {
        console.error("Error sending chat message: ", error);
        throw error;
    }
}


// ---------------- APIS for Files ------------------------------
export const uploadFiles = async (files: File[], sessionId: string, projectId: string) => {
    try {
        const formData = new FormData();

        // Append the files to the FormData object
        files.forEach((file) => {
            formData.append('files', file);
        });

        const response = await fetch(`${API_URL}/knowledge/upload_files?session_id=${sessionId}&project_id=${projectId}`, {
            method: 'POST',
            body: formData,
        });

        // Handle the response
        if (response.ok) {
            const files: FileOutput[] = await response.json();
            const articles: ArticleType[] = files.map(file => {
                return {
                    article_id: file.file_id,
                    article_name: file.file_name,
                    article_type: file.file_type,
                    timestamp: file.created_at,
                    file_path: file.file_path,
                    is_active: file.is_active,
                    is_processing: false,
                }
            })
            console.log('Files uploaded successfully:', articles);
            return articles;
        } else {
            throw new Error(`Upload failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error uploading files:', error);
        throw error;
    } 
}

export const getFiles = async (sessionId: string, projectId: string) => {
    try {
        const response = await fetch(`${API_URL}/knowledge/files?session_id=${sessionId}&project_id=${projectId}`, {
            method: "GET",
        });

        // Handle the response
        if (response.ok) {
            const files: FileOutput[] = await response.json();
            const articles: ArticleType[] = files.map(file => {
                return {
                    article_id: file.file_id,
                    article_name: file.file_name,
                    article_type: file.file_type,
                    timestamp: file.created_at,
                    file_path: file.file_path,
                    is_active: file.is_active,
                    is_processing: false,
                }
            })
            console.log('Files retrieved successfully:', articles);
            return articles;
        } else {
            throw new Error(`Retrieving files failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error retrieving files:', error);
        throw error;
    }
}

export const deleteFile = async (file_id:string, sessionId: string, projectId: string) => {
    try {
        const response = await fetch(`${API_URL}/knowledge/delete_file?file_id=${file_id}&session_id=${sessionId}&project_id=${projectId}`, {
            method: "DELETE",
        });
        return response.json();
    } catch (error) {
        console.error('Error deleting file:', error);
        throw error;
    }
}

export const downloadFile = async (file_id: string, sessionId: string, projectId: string) => {
    try {
        const response = await axios({
            url: `${API_URL}/knowledge/download_file`,
            method: 'GET',
            params: { file_id, session_id: sessionId, project_id: projectId },
            responseType: 'blob',
            timeout: 600000,  // 10 minutes
            onDownloadProgress: (progressEvent) => {
                const total = progressEvent.total;
                const current = progressEvent.loaded;

                if (total) {
                    const percentage = Math.round((current / total) * 100);
                    console.log(`File download progress: ${percentage}%`);
                } else {
                    console.log(`File download progress: ${current} bytes downloaded (total size unknown)`);
                }

                // Check if download has exceeded 10.5 MB
                if (current > 10.5 * 1024 * 1024) {
                    console.log('Download has exceeded 10.5 MB');
                }
            },
        });

        const contentDisposition = response.headers['content-disposition'];
        const fileName = contentDisposition
            ? contentDisposition.split('filename=')[1].replace(/"/g, '')
            : 'downloaded_file';

        // Use FileReader to handle large files
        const reader = new FileReader();
        reader.onload = function(e: ProgressEvent<FileReader>) {
            if (e.target && e.target.result) {
                const link = document.createElement('a');
                if (typeof e.target.result === 'string') {
                    link.href = e.target.result;
                    link.download = fileName;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } else {
                    console.error('FileReader result is not a string');
                }
            } else {
                console.error('FileReader target or result is null');
            }
        };
        reader.onerror = function(e: ProgressEvent<FileReader>) {
            console.error('FileReader error:', e);
        };
        reader.readAsDataURL(response.data);

    } catch (error) {
        if (axios.isAxiosError(error)) {
            if (error.code === 'ECONNABORTED') {
                console.error('Error: The request timed out.');
            } else if (error.response) {
                console.error('Error response:', error.response.status, error.response.data);
            } else if (error.request) {
                console.error('Error request:', error.request);
            } else {
                console.error('Error:', error.message);
            }
        } else {
            console.error('Unexpected error:', error);
        }
    }
};


// ---------------- APIS for Issues ------------------------------
export const draftIssues = async (file_ids: string[], sessionId: string, projectId: string): Promise<IssueType[]> => {
    try {
        const response = await fetch(`${API_URL}/issue/draft_issues?session_id=${sessionId}&project_id=${projectId}`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',  // Ensure the body is treated as JSON
            },
            body: JSON.stringify(file_ids)
        })
        
        const issues: IssueType[] = await response.json();
        console.log("response from draft issues: ",issues)
        return issues
    } catch (error) {
        console.error("Error drafting issues: ", error);
        throw error;
    }
}

export const getIssues = async (sessionId: string, projectId: string) => {
    try {
        const response = await fetch(`${API_URL}/issue/issues?session_id=${sessionId}&project_id=${projectId}`, {
            method: "GET",
        });

        // Handle the response
        if (response.ok) {
            const issues: IssueType[] = await response.json();
            console.log('Issues retrieved successfully:', issues);
            return issues;
        } else {
            throw new Error(`Retrieving issues failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error retrieving issues:', error);
        throw error;
    }
}

export const deleteIssue = async (issue_id:string, sessionId: string, projectId: string) => {
    try {
        const response = await fetch(`${API_URL}/issue/delete_issue?issue_id=${issue_id}&session_id=${sessionId}&project_id=${projectId}`, {
            method: "DELETE",
        });
        return response.json();
    } catch (error) {
        console.error('Error deleting issue:', error);
        throw error;
    }
}

export const createIssue = async (issue_id: string, sessionId: string, projectId: string) => {
    try {
        const response = await fetch(`${API_URL}/issue/create_issue?issue_id=${issue_id}&session_id=${sessionId}&project_id=${projectId}`, {
            method: "POST",
        });
        
        // Handle the response
        if (response.ok) {
            const issue: IssueType = await response.json();
            console.log('Issues created successfully:', issue);
            return issue;
        } else {
            throw new Error(`Creating issue failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error creating issue:', error);
        throw error;
    }
}

// --------------------- RELEASE APIS ---------------------------
export const getReleases = async (sessionId: string, projectId: string) => {
    try {
        const response = await fetch(`${API_URL}/release/releases?session_id=${sessionId}&project_id=${projectId}`, {
            method: "GET",
        });

        // Handle the response
        if (response.ok) {
            const releases: ReleaseType[] = await response.json();
            console.log('Releases retrieved successfully:', releases);
            return releases;
        } else {
            throw new Error(`Retrieving releases failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error retrieving releases:', error);
        throw error;
    }
}

export const getTemplates = async (sessionId: string, projectId: string) => {
    try {
        const response = await fetch(`${API_URL}/release/templates?session_id=${sessionId}&project_id=${projectId}`, {
            method: "GET",
        });

        // Handle the response
        if (response.ok) {
            const templates: TemplateType[] = await response.json();
            console.log('Templates retrieved successfully:', templates);
            return templates;
        } else {
            throw new Error(`Retrieving templates failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error retrieving templates:', error);
        throw error;
    }
}

export const createTemplate = async (template_name: string, template_content:string, sessionId: string, projectId: string): Promise<TemplateType> => {
    try {
        const templateBody: TemplateType = {
            template_id: 'temp-id',
            template_name: template_name,
            template_content: template_content,
            project_id: projectId
        }

        const response = await fetch(`${API_URL}/release/create_template?session_id=${sessionId}&project_id=${projectId}`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',  // Ensure the body is treated as JSON
            },
            body: JSON.stringify(templateBody)
        })
        
        const template: TemplateType = await response.json();
        return template
    } catch (error) {
        console.error("Error drafting issues: ", error);
        throw error;
    }
}

export const createReleaseNote = async (release_name: string, template_id:string, sessionId: string, projectId: string): Promise<string> => {
    try {
        const response = await fetch(`${API_URL}/release/create_release_note?release_name=${release_name}&template_id=${template_id}&session_id=${sessionId}&project_id=${projectId}`, {
            method: "POST"
        })
        
        const note: string = await response.json();
        return note
    } catch (error) {
        console.error("Error creating releaseing note: ", error);
        throw error;
    }
}

// --------------------------------- PROJECT APIS --------------------------------
export const createNewProject = async (project_name: string, project_desc:string, configs: ProjectConfig): Promise<Project> => {
    try {
        const projectBody: Project = {
            project_id: 'temp-id',
            project_name: project_name,
            project_desc: project_desc,
            configs: configs
        }

        const response = await fetch(`${API_URL}/projects/create_project`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',  // Ensure the body is treated as JSON
            },
            body: JSON.stringify(projectBody)
        })
        
        const newProject: Project = await response.json();
        return newProject
    } catch (error) {
        console.error("Error creating new project: ", error);
        throw error;
    }
}

export const getAllProjects = async () => {
    try {
        const response = await fetch(`${API_URL}/projects/all`, {
            method: "GET",
        });

        // Handle the response
        if (response.ok) {
            const projects: Project[] = await response.json();
            console.log('Projects retrieved successfully:', projects);
            return projects;
        } else {
            throw new Error(`Retrieving projects failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error retrieving projects:', error);
        throw error;
    }
}