import React from 'react';
import { Shield, AlertTriangle, Activity, CheckCircle } from 'lucide-react';

const StatusSummary = ({ data }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'Critical':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'Warning':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Normal':
      default:
        return 'bg-green-100 text-green-800 border-green-200';
    }
  };
  
  const getStatusIcon = (status) => {
    switch (status) {
      case 'Critical':
        return <AlertTriangle className="h-6 w-6 text-red-500" />;
      case 'Warning':
        return <AlertTriangle className="h-6 w-6 text-yellow-500" />;
      case 'Normal':
      default:
        return <CheckCircle className="h-6 w-6 text-green-500" />;
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div className="bg-white rounded-lg shadow p-4 flex items-center">
        <div className="rounded-full p-3 bg-blue-100">
          <Activity className="h-6 w-6 text-blue-600" />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-500">Total Traffic</p>
          <p className="text-2xl font-semibold">{((data.totalTraffic)/1024).toFixed(2)} Mbps </p>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow p-4 flex items-center">
        <div className="rounded-full p-3 bg-red-100">
          <Shield className="h-6 w-6 text-red-600" />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-500">Active Threats</p>
          <p className="text-2xl font-semibold">{data.activeThreats}</p>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow p-4 flex items-center">
        <div className="rounded-full p-3 bg-orange-100">
          <AlertTriangle className="h-6 w-6 text-orange-600" />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-500">Critical Alerts</p>
          <p className="text-2xl font-semibold">{data.criticalAlerts}</p>
        </div>
      </div>
      
      <div className={`rounded-lg shadow p-4 flex items-center ${getStatusColor(data.systemStatus)}`}>
        <div className="rounded-full p-3 bg-white bg-opacity-60">
          {getStatusIcon(data.systemStatus)}
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium">System Status</p>
          <p className="text-2xl font-semibold">{data.systemStatus}</p>
        </div>
      </div>
    </div>
  );
};

export default StatusSummary;