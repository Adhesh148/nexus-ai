import './ChatHistory.scss'

import { Button } from '@mui/material';
import ChatHistoryLabel from './ChatHistoryLabel';
import { useChatStore } from '../../../stores/chatStore';

export default function ChatHistory() {  
    
    const chatSessions = useChatStore((state) => state.chatSessions);
    const now = new Date();
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(now.getDate() - 7);
    const recentChatSessions = chatSessions.filter((session) =>  session.creation_time >= sevenDaysAgo)
    const olderChatSessions = chatSessions.filter((session) =>  session.creation_time < sevenDaysAgo)

    return (
        <div className="chat-history">
            <div className="chat-history-header">
                <Button variant="contained" fullWidth ><span style={{fontSize: '16px', textTransform: 'none'}}>New Chat</span></Button>
            </div>

            <div className="chat-history-body">
                <div className="chat-history-body-heading">Recent</div>
                {
                   recentChatSessions.map((session, ) => (
                        <ChatHistoryLabel session={session} key={session.session_id}/>
                   )) 
                }
                <div style={{marginTop: '20px'}}></div>
                <div className="chat-history-body-heading">Older</div>
                {
                   olderChatSessions.map((session, indx) => (
                        <ChatHistoryLabel session={session} key={session.session_id}/>
                   ))
                }
            </div>
        </div>
    )
}