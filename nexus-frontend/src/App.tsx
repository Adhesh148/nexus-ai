import React, { useEffect } from 'react';
import { Amplify } from 'aws-amplify';
import { useAuthenticator, withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui/dist/styles.css';
import Home from './components/Home/Home';
import { Route, Routes } from 'react-router-dom';

import './App.css';
import Header from './components/Header/Header';
import Navbar from './components/Navbar/Navbar';

import awsconfig from './aws-exports';
import Chat from './components/Chat/Chat';
import KnowledgeBase from './components/KnowledgeBase/KnowledgeBase';
import Stories from './components/Stories/Stories';
import Releases from './components/Releases/Releases';
import Development from './components/Development/Development';
import { useProjectStore } from './stores/projectStore';

Amplify.configure(awsconfig);

function App() {

  const { user } = useAuthenticator((context) => [context.user]);
  const getProjects = useProjectStore(state => state.getProjects)

  useEffect(() => {
    if (user) {
      // Perform post-sign-in actions here
      console.log('User signed in:', user.signInDetails?.loginId);
      getProjects();
    }
  }, [user, getProjects]);
  
  return (
          <div className="App">
            <Header />
            <div className="app-body">
              <div className="app-navbar">
                <Navbar />
              </div>
              <div className="app-main-content">
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/chat" element={<Chat />} />
                  <Route path="/knowledge-base" element={<KnowledgeBase />} />
                  <Route path="/stories" element={<Stories />} />
                  <Route path="/releases" element={<Releases />} />
                  <Route path="/development" element={<Development />} />
                </Routes>
              </div>
            </div>
          </div>
  );
}

export default withAuthenticator(App);