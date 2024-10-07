import * as React from 'react';
import './Chat.scss'
import ChatHistory from './ChatHistory/ChatHistory';
import ChatContainer from './ChatContainer/ChatContainer';
import ChatInput from './ChatInput/ChatInput';

export default function Chat() {
    return (
        <div className="chat-page">
            <div className="chat-layout">
                <div className="chat-main-layout">
                    <ChatContainer />
                    <ChatInput />
                </div>
                <div className="chat-history-layout">
                    <ChatHistory />
                </div>
            </div>
        </div>
    )
}