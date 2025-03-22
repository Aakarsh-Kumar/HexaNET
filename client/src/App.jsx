import React from 'react';
import Dashboard from './components/Dashboard';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import './App.css';

function App() {
  return (
    <div className="flex h-screen bg-grey-100">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-4">
          <Dashboard />
        </main>
      </div>
    </div>
  );
}
export default App;