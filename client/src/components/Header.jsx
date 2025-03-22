import React from 'react';
import { Bell, Menu, Search, User } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm z-10">
      <div className="flex items-center justify-between px-6 py-3">
        <div className="flex items-center md:hidden">
          <button className="text-gray-500 hover:text-gray-700">
            <Menu size={24} />
          </button>
        </div>
        
        <div className="flex items-center rounded-lg bg-gray-100 px-3 py-2 w-64">
          <Search size={18} className="text-gray-400" />
          <input
            className="ml-2 w-full bg-transparent outline-none text-gray-700 placeholder-gray-500"
            type="text"
            placeholder="Search..."
          />
        </div>
        
        <div className="flex items-center">
          <button className="relative p-2 text-gray-500 hover:text-gray-700">
            <Bell size={20} />
            <span className="absolute top-0 right-0 h-4 w-4 text-xs flex items-center justify-center bg-red-500 text-white rounded-full">3</span>
          </button>
          
          <div className="ml-4 flex items-center">
            <div className="h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center">
              <User size={16} className="text-gray-600" />
            </div>
            <span className="ml-2 font-medium text-gray-700">Admin</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;