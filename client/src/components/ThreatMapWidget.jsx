import React, { useEffect, useRef, useState } from 'react';
import { fetchGeographicThreats } from '../api/mockData';
import { Link } from 'react-router-dom';

const ThreatMapWidget = () => {
  const mapRef = useRef(null);
  const [threatData, setThreatData] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        const data = await fetchGeographicThreats(10);
        setThreatData(data);
      } catch (err) {
        console.error('Failed to fetch threat map data for widget', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    if (!mapRef.current || loading || !threatData.length) return;
    

    const mapCanvas = mapRef.current;
    const ctx = mapCanvas.getContext('2d');
    

    ctx.fillStyle = document.body.classList.contains('dark') ? '#374151' : '#f3f4f6';
    ctx.fillRect(0, 0, mapCanvas.width, mapCanvas.height);

    threatData.forEach(threat => {
      const x = (parseFloat(threat.longitude) + 180) * (mapCanvas.width / 360);
      const y = (90 - parseFloat(threat.latitude)) * (mapCanvas.height / 180);
      
      const color = getSeverityColor(threat.severity);
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, 2 * Math.PI);
      ctx.fill();
      
      ctx.beginPath();
      ctx.arc(x, y, 8, 0, 2 * Math.PI);
      ctx.fillStyle = `${color}33`; 
      ctx.fill();
    });
    
  }, [threatData, loading]);

  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical': return '#dc2626';
      case 'high': return '#ea580c';
      case 'medium': return '#eab308';
      case 'low': return '#3b82f6';
      default: return '#6b7280';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="w-full h-64 relative">
      <canvas 
        ref={mapRef} 
        className="w-full h-full rounded-lg"
        width={400}
        height={200}
      ></canvas>
      
      <div className="absolute bottom-2 right-2">
        <Link 
          to="/threat-map" 
          className="px-3 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          View Full Map
        </Link>
      </div>
      
      <div className="absolute top-2 left-2 bg-white dark:bg-gray-800 bg-opacity-80 dark:bg-opacity-80 px-2 py-1 rounded text-sm text-gray-800 dark:text-white">
        {threatData.length} Active Threats
      </div>
    </div>
  );
};

export default ThreatMapWidget;