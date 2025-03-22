import React, { useState, useEffect } from 'react';
import TrafficChart from './TrafficChart';
import AlertTable from './AlertTable';
import ThreatMap from './ThreatMap';
import StatusSummary from './StatusSummary';
import axios from 'axios';

const Dashboard = () => {
  const [networkData, setNetworkData] = useState({
    traffic: [],
    alerts: [],
    threats: [],
    summary: {
      totalTraffic: 0,
      activeThreats: 0,
      criticalAlerts: 0,
      systemStatus: 'Normal'
    }
  });

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 10000);
    return () => clearInterval(interval);
  }, []);
  
  const fetchDashboardData = async () => {
    try {
      const dashboardResponse = await axios.get('/api/dashboard');
      setNetworkData(dashboardResponse.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };
  
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Network Security Dashboard</h1>
      
      <StatusSummary data={networkData.summary} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Network Traffic</h2>
          <TrafficChart data={networkData.traffic} />
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Threat Map</h2>
          <ThreatMap threats={networkData.threats} />
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow">
        <div className="p-6">
          <h2 className="text-lg font-semibold mb-4">Recent Alerts</h2>
          <AlertTable alerts={networkData.alerts} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;