import { useState } from 'react';
import './ChatInput.scss'
import { IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { useChatStore } from '../../../stores/chatStore';
import StopCircleIcon from '@mui/icons-material/StopCircle';

export default function ChatInput() {

    const [message, setMessage] = useState("");
    const sendMessage = useChatStore((state) => state.sendMessage);
    const loading = useChatStore((state) => state.loading);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setMessage(e.target.value);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await sendMessage(message); // Send the message using Zustand's action
        setMessage(""); // Clear the input after sending
      };

    return (
        <div className="chat-input">
            <form className="chat-input-wrapper" onSubmit={handleSubmit}>
                <input
                    type="text"
                    className="chat-input-field"
                    value={message}
                    onChange={handleInputChange}
                    placeholder="Message NexusAI"
                    disabled={loading}
                />
                <IconButton aria-label="send" type="submit">
                    {loading ? <StopCircleIcon sx={{ fontSize: 30 }} /> : <SendIcon sx={{ fontSize: 30 }} />}
                </IconButton>
            </form>
        </div>
    )
}