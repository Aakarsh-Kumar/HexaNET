import React from 'react';
import { LineChart, Line } from 'recharts';
import { CartesianGrid } from 'recharts';
import { XAxis } from 'recharts';
import { YAxis } from 'recharts';
import { Tooltip } from 'recharts';
import { Legend } from 'recharts';

const TrafficChart = ({ data }) => {
  if (!data || !data.labels || !data.datasets) {
    return <div className="flex justify-center items-center h-64 bg-gray-50">No traffic data available</div>;
  }

  const chartData = data.labels.map((label, index) => {
    const point = { name: label };
    
    data.datasets.forEach(dataset => {
      point[dataset.label] = dataset.data[index];
    });
    
    return point;
  });

  return (
    <div className="h-64">
      <LineChart
        width={500}
        height={250}
        data={chartData}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        {data.datasets.map((dataset, index) => (
          <Line
            key={index}
            type="monotone"
            dataKey={dataset.label}
            stroke={dataset.borderColor}
            fill={dataset.backgroundColor}
            activeDot={{ r: 8 }}
          />
        ))}
      </LineChart>
      
      <div className="mt-4 text-sm text-gray-500">
        <div className="flex items-center justify-between">
          <div>Last updated: {new Date().toLocaleTimeString()}</div>
          <div className="flex items-center">
            <button className="px-3 py-1 bg-blue-100 text-blue-600 rounded hover:bg-blue-200">
              Live
            </button>
            <button className="ml-2 px-3 py-1 text-gray-600 rounded hover:bg-gray-100">
              24h
            </button>
            <button className="ml-2 px-3 py-1 text-gray-600 rounded hover:bg-gray-100">
              7d
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrafficChart;