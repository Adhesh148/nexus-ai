import { create } from 'zustand'
import { Project, ProjectConfig } from '../types/ProjectType'
import { createNewProject, getAllProjects } from '../utils/apiClient';
import { useChatStore } from './chatStore';

export interface ProjectStoreState {
    projects: Project[];
    newProjectDialogOpen: boolean;
    currentProjectId: string;

    addProject: (projectName: string, projectDesc: string, configs: ProjectConfig) => Promise<Project>;
    getProjects: () => Promise<void>;
    toggleNewProjectDialog: () => void;
    toggleCurrentProject: (projectId: string) => void;
}

export const useProjectStore = create<ProjectStoreState>((set, get) => ({
    projects: [],
    newProjectDialogOpen: false,
    currentProjectId: "101",

    // Add a new project
    addProject: async (projectName: string, projectDesc: string, configs: ProjectConfig) => {

        try {
            const newProject: Project = await createNewProject(projectName, projectDesc, configs);
            console.log("Created project: ", newProject)
            set(state => {
                return {
                    ...state,
                    projects: [...state.projects, newProject],
                    currentProjectId: newProject.project_id
                }
            });

            return newProject;
        } catch (error) {
            console.error('Error creating new project:', error);
            throw error;
        }
    },

    getProjects: async () => {
        try {
            const projects: Project[] = await getAllProjects();
            set(state => {
                return {
                    ...state,
                    projects: projects,
                }
            });
        } catch (error) {
            console.error('Error retrieving projects:', error);
            throw error;
        }
    },

    // Toggle the new project dialog
    toggleNewProjectDialog: () => {
        set((state) => {
            const newState = !state.newProjectDialogOpen;
            console.log('New Project Dialog is now', newState ? 'open' : 'closed');
            return {
                ...state,
                newProjectDialogOpen: newState
            }
        })
    },

    toggleCurrentProject: (projectId: string) => {
        console.log('Changing current project to', projectId);
        set((state) => {
            return {
                ...state,
                currentProjectId: projectId
            }
        })

        try {
            // Create new chat session for the project
            const createChatSession = useChatStore.getState().createNewSession;
            createChatSession();
          } catch (error) {
            console.error('Failed to create new chat session:', error);
          }
    }

}));