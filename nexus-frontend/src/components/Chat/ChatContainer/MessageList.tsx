import Message from './Message';
import { cn } from '../../../utils/utils'
import { useChatStore } from '../../../stores/chatStore';
import { useEffect, useRef } from 'react';

export default function MessageList() {

    const chatMessages = useChatStore((state) => state.chatMessages);
    const messagesEndRef = useRef<null | HTMLDivElement>(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(() => {
        scrollToBottom()
      }, [chatMessages]);
    
    return (
        <div className={cn('w-full h-3/4 mx-auto')}>
            <div className='overflow-y-auto h-full pr-0 pl-0' >
                {
                    chatMessages.map((msg, index) => (
                        <Message
                            id={msg.id}
                            key={'msg-' + msg.id}
                            msg={msg}
                            className={index === 0 ? 'pt-4' : ''}
                        />
                    ))
                }
                <div ref={messagesEndRef} />
            </div>
        </div>
    )
}