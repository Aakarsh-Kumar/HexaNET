import React from 'react';
import { Shield, MapPin } from 'lucide-react';

const ThreatMap = ({ threats }) => {
  
  const activeThreats = threats.filter(threat => threat.status === 'Active');
  
  return (
    <div className="relative h-64 bg-gray-200 rounded overflow-hidden">
      <div className="absolute inset-0 opacity-30 bg-blue-100">
        <div className="absolute top-1/4 left-1/4 w-1/6 h-1/6 bg-gray-400 rounded-lg"></div>
        <div className="absolute top-1/3 left-1/2 w-1/5 h-1/4 bg-gray-400 rounded-lg"></div>
        <div className="absolute top-2/3 left-1/6 w-1/6 h-1/6 bg-gray-400 rounded-lg"></div>
        <div className="absolute top-1/2 left-2/3 w-1/8 h-1/5 bg-gray-400 rounded-lg"></div>
      </div>

      {activeThreats.map((threat, index) => {
        const ipParts = threat.source.split('.');
        const xPercent = (parseInt(ipParts[0]) * parseInt(ipParts[2])) % 80 + 10;
        const yPercent = (parseInt(ipParts[1]) * parseInt(ipParts[3])) % 80 + 10;
        
        return (
          <div 
            key={threat.id}
            className="absolute transform -translate-x-1/2 -translate-y-1/2 z-10"
            style={{ 
              left: `${xPercent}%`, 
              top: `${yPercent}%`,
              animation: `pulse 1.5s infinite ${index * 0.2}s`
            }}
          >
            <div className={`
              p-1 rounded-full 
              ${threat.impact === 'High' ? 'bg-red-500' : 
                threat.impact === 'Medium' ? 'bg-orange-500' : 'bg-yellow-500'}
            `}>
              <MapPin size={16} className="text-white" />
            </div>
          </div>
        );
      })}
      
      <div className="absolute bottom-2 right-2 bg-white bg-opacity-80 p-2 rounded text-xs">
        <div className="font-semibold mb-1">Threat Impact</div>
        <div className="flex items-center">
          <div className="w-3 h-3 rounded-full bg-red-500 mr-1"></div>
          <span>High</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 rounded-full bg-orange-500 mr-1"></div>
          <span>Medium</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 rounded-full bg-yellow-500 mr-1"></div>
          <span>Low</span>
        </div>
      </div>
      
      {activeThreats.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-70">
          <div className="flex items-center text-green-600">
            <Shield size={24} />
            <span className="ml-2 font-medium">No active threats detected</span>
          </div>
        </div>
      )}

     
    </div>
  );
};

export default ThreatMap;