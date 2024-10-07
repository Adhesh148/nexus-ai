import { create } from "zustand";
import { ArticleType } from "../types/KnowledgeType";
import { uploadFiles, getFiles, deleteFile, downloadFile } from "../utils/apiClient";
import { useProjectStore } from "./projectStore";

export interface KnowledgeState {
    articles: ArticleType[];

    // actions
    addArticles: (files: File[]) => Promise<ArticleType[]>;
    getArticles: () => Promise<void>;
    downloadArticle: (file_id: string) => Promise<void>;
    deleteArticle: (file_id: string) => Promise<void>;
}

export const useKnowledgeStore = create<KnowledgeState>((set, get) => ({
    // state
    articles: [],

    addArticles: async (files: File[]) => {
        try {

            // Enter entry first
            set(state => {
                const newArticles: ArticleType[]  = files.map(file => {
                    const newArticle: ArticleType = {
                        article_id: 'temp-id',
                        article_name: file.name,
                        article_type: file.type,
                        is_processing: true,
                        timestamp: '',
                        file_path: '',
                        is_active: true
                    }     
                    return newArticle;
                })
                  
                return {
                    ...state,
                    articles: [...state.articles, ...newArticles]
                }
            });

            const projectId = useProjectStore.getState().currentProjectId;
            const articles: ArticleType[] = await uploadFiles(files, '1', projectId)
            console.log("Uploaded files")

            set(state => { 
                const otherArtciles: ArticleType[] = state.articles.filter((article) => article.article_id !== 'temp-id')       
                return {
                    ...state,
                    articles: [...otherArtciles, ...articles]
                }
            });

            return articles
        } catch (error) {
            console.error('Error uploading files:', error);
            throw error;
        }
    },

    getArticles: async () => {
        try {
            const projectId = useProjectStore.getState().currentProjectId;
            const articles: ArticleType[] = await getFiles('1', projectId)
            console.log("Retrieved files: ", articles)
            
            set(state => {        
                return {
                    ...state,
                    articles: articles,
                }
            });
        } catch (error) {
            console.error('Error retrieving files:', error);
            throw error;
        }
    },

    downloadArticle: async (file_id: string) => {
        try {
            const projectId = useProjectStore.getState().currentProjectId;
            const response = await downloadFile(file_id, '1', projectId);
            console.log('Downloaded file:', response);
        } catch (error) {
            console.error('Error downloading file:', error);
            throw error;
        }
    },

    deleteArticle: async (file_id: string) => {
        try {
            const projectId = useProjectStore.getState().currentProjectId;
            const status = await deleteFile(file_id, '1', projectId);

            console.log("delete status: ", status)
            if (status === true) {
                set(state => {        
                    return {
                        ...state,
                        articles: state.articles.filter((file) => file.article_id !== file_id),
                    }
                });
            }
            
        } catch (error) {
            console.error('Error deleting file:', error);
            throw error;
        }
    }
}))