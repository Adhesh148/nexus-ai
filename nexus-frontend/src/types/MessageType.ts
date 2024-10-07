export const MessageRoleEnum = {
    System: 'system',
    User: 'user',
    AI: 'ai',
} as const

export type MessageRole = (typeof MessageRoleEnum)[keyof typeof MessageRoleEnum]

export type SessionType = 'chat'

export interface Message {
    id: string
    role: MessageRole
    content: string
    generating?: boolean
    timestamp?: string
}

export interface ChatSession {
    session_id: string;
    session_name: string;
    creation_time: Date;
    is_active: boolean;
    is_favorite?: boolean;
}