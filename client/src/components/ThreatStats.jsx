import React from 'react';
import { ShieldAlert, ShieldCheck, Clock, AlertCircle } from 'lucide-react';

const ThreatStats = ({ stats }) => {
  const statCards = [
    {
      title: 'Total Threats',
      value: stats.totalThreats,
      icon: <ShieldAlert size={24} className="text-blue-500" />,
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
      textColor: 'text-blue-700 dark:text-blue-300'
    },
    {
      title: 'Critical Threats',
      value: stats.criticalThreats,
      icon: <AlertCircle size={24} className="text-red-500" />,
      bgColor: 'bg-red-50 dark:bg-red-900/20',
      textColor: 'text-red-700 dark:text-red-300'
    },
    {
      title: 'Resolved',
      value: stats.resolvedThreats,
      icon: <ShieldCheck size={24} className="text-green-500" />,
      bgColor: 'bg-green-50 dark:bg-green-900/20',
      textColor: 'text-green-700 dark:text-green-300'
    },
    {
      title: 'Pending',
      value: stats.pendingThreats,
      icon: <Clock size={24} className="text-yellow-500" />,
      bgColor: 'bg-yellow-50 dark:bg-yellow-900/20',
      textColor: 'text-yellow-700 dark:text-yellow-300'
    }
  ];

  return (
    <>
      {statCards.map((card, index) => (
        <div 
          key={index}
          className={`rounded-lg shadow-md p-4 ${card.bgColor}`}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">{card.title}</p>
              <p className={`text-2xl font-bold ${card.textColor}`}>{card.value}</p>
            </div>
            <div>
              {card.icon}
            </div>
          </div>
        </div>
      ))}
    </>
  );
};

export default ThreatStats;