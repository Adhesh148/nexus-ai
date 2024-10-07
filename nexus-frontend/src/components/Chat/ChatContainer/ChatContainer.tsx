import { TypeAnimation } from 'react-type-animation';
import { useChatStore } from '../../../stores/chatStore';
import './ChatContainer.scss'
import MessageList from './MessageList'


export default function ChatContainer() {
    const chatMessages = useChatStore((state) => state.chatMessages);

    return (
        <div className="chat-container">
            {
                (chatMessages.length === 0) && (
                    <div className="chat-home">
                        <div className="chat-home-img-div">
                            <img src={require('../../../assets/images/logo_6.png')} alt="Logo" className="logo-img" width="120" height="120"/>
                        </div>
                        <div className="chat-home-labels">
                            <div className="chat-home-label">
                            <span className="highlight">Ask Docs </span>
                            <TypeAnimation
                                sequence={[
                                    'What is my product architecture?',
                                    1500,
                                    'How to raise a support ticket?',
                                    1500,
                                    'Help me with onboarding',
                                    1500,
                                    'Get me the documentation of ABC',
                                    1500,
                                ]}
                                speed={50}
                                style={{
                                    fontSize: '16px',
                                }}
                                repeat={Infinity}
                                />
                            </div>
                            <div className="chat-home-label"> 
                                <span className="highlight">Ask Code </span>
                                <TypeAnimation
                                    sequence={[
                                        'How does my GraphQL work?',
                                        2000,
                                        'Explain how the service works?',
                                        2000,
                                        'Tell me what is wrong with ABC module?',
                                        2000,
                                        'Add test cases for XYZ module',
                                        2000,
                                    ]}
                                    speed={50}
                                    style={{
                                        fontSize: '16px',
                                    }}
                                    repeat={Infinity}
                                    />
                            </div>
                            <div className="chat-home-label"> 
                                <span className="highlight">Ask Knowledge Base </span>
                                <TypeAnimation
                                    sequence={[
                                        'Summarize document',
                                        2500,
                                        'Translate document to French',
                                        2500,
                                        'What are the requirements listed?',
                                        2500,
                                        'Search for references in the document',
                                        2500,
                                    ]}
                                    speed={50}
                                    style={{
                                        fontSize: '16px',
                                    }}
                                    repeat={Infinity}
                                    />
                            </div>
                        </div>
                    </div>
                )
            }
            <MessageList />
        </div>
    ) 
}