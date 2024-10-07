import { create } from "zustand";
import { Message, MessageRoleEnum, ChatSession } from "../types/MessageType";
import {v4 as uuidv4} from "uuid";
import { sendChatMessage } from "../utils/apiClient";
import { useProjectStore } from "./projectStore";

// Sample data for chat sessions
const sampleChatSessions: ChatSession[] = [
    {
        session_id: '1',
        session_name: 'Sass Style for Paragraph',
        creation_time: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
        is_active: true,
        is_favorite: true
    },
    {
        session_id: '2',
        session_name: 'Docker Compose Syntax Help',
        creation_time: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // 1 day ago
        is_active: true
    },
    {
        session_id: '3',
        session_name: 'Remove Podman Alias Windows',
        creation_time: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000), // 6 days ago
        is_active: true
    },
    {
        session_id: '4',
        session_name: 'PyMySQL Fetchall Issues',
        creation_time: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000), // 4 days ago
        is_active: true,
        is_favorite: false
    },
    {
        session_id: '5',
        session_name: 'Highlight Selected List Item',
        creation_time: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000), // 15 days ago
        is_active: false
    },
    {
        session_id: '6',
        session_name: 'WSL Shutdown Command Explained',
        creation_time: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // 30 days ago
        is_active: false,
        is_favorite: true
    }
];


export interface ChatState {
  chatSessionId: string;
  chatMessages: Message[];
  chatSessions: ChatSession[]
  loading: boolean;
  // Actions
  sendMessage: (content: string) => Promise<void>;
  setLoading: (loading: boolean) => void;
  startNewSessionIfNeeded: () => Promise<void>;
  addMessage: (message: Message) => void;
  createNewSession: () => Promise<void>;
  fetchChatSessions: () => Promise<void>;
  resetChat: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  // State
  chatSessionId: uuidv4(),
  chatMessages: [],
  loading: false,
  chatSessions: sampleChatSessions,

  // Action to set loading state
  setLoading: (loading) => set({ loading }),

  fetchChatSessions: async () => {
    // replace with API call
    const sessions: ChatSession[] = sampleChatSessions;
    set({chatSessions: sessions})
  },

  // Action to send a message
  sendMessage: async (content: string) => {
    const state = get();

    // Ensure chat session is started
    if (state.chatSessionId === null) {
      await state.startNewSessionIfNeeded();
    }

    set(state => {
        const newUserMessage: Message = {id: uuidv4(), role: MessageRoleEnum.User, content: content, generating: false};
        const newAIMessage: Message = {id: 'temp-message-id', role: MessageRoleEnum.AI, content: "", generating: true};

        return {
            ...state,
            chatMessages: [...state.chatMessages, newUserMessage, newAIMessage],
            loading: true
        }
    });

    try {
      const projectId = useProjectStore.getState().currentProjectId;
      const response = await sendChatMessage({
        input: {
            input: content
        }
      }, state.chatSessionId, projectId)

      // Simulate a response message from the server
      const responseMessage: Message = {
        id: Date.now().toString(),
        content: response.output.output,
        role: MessageRoleEnum.User,
        timestamp: new Date().toISOString(),
      };

      set(state => {
            const updatedChatMessages = state.chatMessages.map(msg => msg.generating ? {
                    ...msg,
                    id: uuidv4(),
                    content: responseMessage.content,
                    generating: false
                } : msg
            );

            return {
                ...state,
                chatMessages: updatedChatMessages,
                loading: false
            }
        });

      
    } catch (error) {
        console.error("Failed to send message:", error);
        set(state => ({
            chatMessages: state.chatMessages.filter(msg => msg.id !== 'temp-message-id'),
            loading: false
        }));
    }
  },

  // Action to start a new session if needed
  startNewSessionIfNeeded: async () => {
    const state = get();
    if (state.chatSessionId === null) {
      await state.createNewSession();
    }
  },

  // Action to create a new session
  createNewSession: async () => {
    set({ loading: true });

    try {
      // Replace this with your actual API call
      const newSessionId = uuidv4(); // Example session ID

      set({ chatSessionId: newSessionId, chatMessages: [] });
    } catch (error) {
      console.error("Failed to create a new session:", error);
    } finally {
      set({ loading: false });
    }
  },

  // Action to add a message to the chat
  addMessage: (message: Message) => {
    set((state) => ({
      chatMessages: [...state.chatMessages, message],
    }));
  },

  // Action to reset the chat state
  resetChat: () => {
    set({
      chatSessionId: uuidv4(),
      chatMessages: [],
      loading: false,
    });
  },
}));
