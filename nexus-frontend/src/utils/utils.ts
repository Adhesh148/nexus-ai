import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { ConfluenceConfig, GithubConfig, JiraConfig } from '../types/ProjectType'

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
}

export function parseJsonOrEmpty(json: string): any {
    try {
        return JSON.parse(json)
    } catch (e) {
        return {}
    }
}

// Type Guard Functions
export function isGithubConfig(obj: any): obj is GithubConfig {
    return obj.platform === 'github' && typeof obj.accessToken === 'string' && typeof obj.repoName === 'string';
}

export function isConfluenceConfig(obj: any): obj is ConfluenceConfig {
    return obj.platform === 'confluence' && typeof obj.username === 'string' && typeof obj.url === 'string' && typeof obj.token === 'string';
}

export function isJiraConfig(obj: any): obj is JiraConfig {
    return obj.platform === 'jira' && typeof obj.username === 'string' && typeof obj.url === 'string' && typeof obj.token === 'string' && typeof obj.projectKey === 'string';
}

// Generic parsing and validation function
export function parseAndValidateConfig<T>(
    jsonString: string,
    typeGuard: (obj: any) => obj is T
): T {
    try {
        const obj = JSON.parse(jsonString);
        if (typeGuard(obj)) {
            return obj;
        } else {
            throw new Error('Object does not match the expected type.');
        }
    } catch (error) {
        console.error('Failed to parse JSON or validate type:', error);
        throw error; // Rethrow the error to ensure the caller is aware of the failure
    }
}