// Base configuration interface for common properties
interface BaseConfig {
    platform: 'github' | 'jira' | 'confluence';
}

// Specific configuration interfaces extending BaseConfig
export interface GithubConfig extends BaseConfig {
    platform: 'github';
    token: string;
    repoName: string;
}

export interface ConfluenceConfig extends BaseConfig {
    platform: 'confluence';
    username: string;
    url: string;
    token: string;
}

export interface JiraConfig extends BaseConfig {
    platform: 'jira';
    username: string;
    url: string;
    token: string;
    projectKey: string;
}

// Dictionary type for platform-specific configurations
export type ProjectConfig = {
    github?: GithubConfig;
    confluence?: ConfluenceConfig;
    jira?: JiraConfig;
};

// Project interface including a list of configurations
export interface Project {
    project_id: string;
    project_name: string;
    project_desc: string | null;
    configs: ProjectConfig;
}