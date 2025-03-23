import React from 'react';
import { Shield, Wifi, AlertTriangle, Settings, FileText, Home } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { name: 'Dashboard', icon: <Home size={20} /> },
    { name: 'Threats', icon: <Shield size={20} /> },
    { name: 'Alerts', icon: <AlertTriangle size={20} /> },
    { name: 'Reports', icon: <FileText size={20} /> },
    { name: 'Settings', icon: <Settings size={20} /> }
  ];

  return (
    <div className="bg-gray-900 text-white w-64 flex-shrink-0 hidden md:block">
      <div className="flex items-center justify-center h-16 border-b border-gray-800">
        <div className="flex items-center">
          <Shield className="text-blue-500 h-8 w-8" />
          <span className="ml-2 text-xl font-semibold">HexaNET </span>
        </div>
      </div>
      <nav className="mt-6">
        {navItems.map((item, index) => (
          <a
            key={index}
            href="#"
            className={`flex items-center px-6 py-3 text-gray-300 hover:bg-gray-800 hover:text-white ${
              index === 0 ? 'bg-gray-800 text-white' : ''
            }`}
          >
            {item.icon}
            <span className="mx-3">{item.name}</span>
          </a>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;