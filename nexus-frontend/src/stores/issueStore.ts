import { create } from "zustand";
import { IssueType } from "../types/IssueType";
import { createIssue, deleteIssue, draftIssues, getIssues } from "../utils/apiClient";
import { useProjectStore } from "./projectStore";

export interface IssueState {
    issues: IssueType[];
    loading: boolean;

    // actions
    draftIssues: (article_ids: string[]) => Promise<IssueType[]>;
    getIssues: () => Promise<void>;
    setLoading: (loading: boolean) => void;
    deleteIssue: (issue_id: string) => Promise<void>;
    createIssue: (issue_id: string) => Promise<IssueType>;
}

export const useIssueStore = create<IssueState>((set, get) => ({
    issues: [],
    loading: false,

    setLoading: (loading) => set({ loading }),
    draftIssues: async (article_ids: string[]) => {
        
        try {
            const state = get()
            state.setLoading(true)
            const projectId = useProjectStore.getState().currentProjectId;
            const issues: IssueType[] = await draftIssues(article_ids, '1', projectId)
            console.log("Retrieved issues: ", issues)
            set(state => {
                return {
                    ...state,
                    issues: [...state.issues, ...issues],
                    loading: false
                }
            });
            return issues;
        } catch (error) {
            console.error('Error drafting issues:', error);
            throw error;
        }
    },

    getIssues: async () => {
        try {
            const state = get()
            state.setLoading(true)
            const projectId = useProjectStore.getState().currentProjectId;
            const issues: IssueType[] = await getIssues('1', projectId)
            console.log("Retrieved issues: ", issues)
            
            set(state => {        
                return {
                    ...state,
                    issues: issues,
                    loading: false
                }
            });
        } catch (error) {
            console.error('Error retrieving issues:', error);
            throw error;
        }
    },

    deleteIssue: async (issue_id: string) => {
        try {
            const projectId = useProjectStore.getState().currentProjectId;
            const status = await deleteIssue(issue_id, '1', projectId);

            console.log("delete status: ", status)
            if (status === true) {
                set(state => {        
                    return {
                        ...state,
                        issues: state.issues.filter((issue) => issue.issue_id !== issue_id),
                    }
                });
            }
            
        } catch (error) {
            console.error('Error deleting issue:', error);
            throw error;
        }
    },

    createIssue: async (issue_id: string) => {
        try {
            const state = get()
            state.setLoading(true)
            
            const projectId = useProjectStore.getState().currentProjectId;
            const newIssue = await createIssue(issue_id, '1', projectId);

            set(state => {        
                return {
                    ...state,
                    issues: [...state.issues.filter((issue) => issue.issue_id !== issue_id), newIssue],
                    loading: false
                }
            });

            return newIssue;
        } catch (error) {
            console.error('Error creating issue:', error);
            throw error;
        }
    }

}))