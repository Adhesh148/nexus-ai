import { create } from "zustand";
import { ReleaseType, TemplateType } from "../types/TemplateTypes";
import { createReleaseNote, createTemplate, getReleases, getTemplates } from "../utils/apiClient";
import { useProjectStore } from "./projectStore";

export interface ReleaesStoreState {
    releases: ReleaseType[];
    templates: TemplateType[];
    loading: boolean;
    generatedReleaseNote: string;

    getReleases: () => Promise<void>;
    getTemplates: () => Promise<void>;
    setLoading: (loading: boolean) => void;
    createTemplate: (template_name: string, template_content: string) => Promise<TemplateType>;
    generateReleaseNote: (release_name: string, template_id:string) => Promise<string>;
}

export const useReleaseStore = create<ReleaesStoreState>((set, get) => ({
    releases: [],
    templates: [],
    loading: false,
    generatedReleaseNote: 'Your generated template will appear here ...',

    setLoading: (loading) => set({ loading }),
    getReleases: async () => {
        try {
            const projectId = useProjectStore.getState().currentProjectId;
            const releases: ReleaseType[] = await getReleases('1', projectId);
            set(state => {        
                return {
                    ...state,
                    releases: releases
                }
            });

        } catch (error) {
            console.error('Error retrieving releases:', error);
            throw error;
        }
    },

    getTemplates: async () => {
        try {
            const projectId = useProjectStore.getState().currentProjectId;
            const templates: TemplateType[] = await getTemplates('1', projectId);
            set(state => {        
                return {
                    ...state,
                    templates: templates
                }
            });

        } catch (error) {
            console.error('Error retrieving templates:', error);
            throw error;
        }
    },

    createTemplate: async (template_name: string, template_content: string) => {
        try {
            const state = get();

            state.setLoading(true);
            const projectId = useProjectStore.getState().currentProjectId;
            const newTemplate: TemplateType = await createTemplate(template_name, template_content, '1', projectId);
            set(state => {        
                return {
                    ...state,
                    templates: [...state.templates, newTemplate],
                    loading: false
                }
            });

            return newTemplate;
        } catch (error) {
            console.error('Error creating template:', error);
            throw error;
        }
    },

    generateReleaseNote: async (release_name: string, template_id:string) => {
        try {
            const state = get();
            state.setLoading(true);

            const projectId = useProjectStore.getState().currentProjectId;
            const releaseNote: string = await createReleaseNote(release_name, template_id, '1', projectId); 
            console.log("generated release note: ",releaseNote)

            set(state => {        
                return {
                    ...state,
                    generatedReleaseNote: releaseNote,
                    loading: false
                }
            });
            return releaseNote
        } catch (error) {
            console.error('Error generating release note:', error);
            throw error;
        }
    }


}))