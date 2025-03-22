import React, { useState } from 'react';
import { ChevronDown, ChevronUp, AlertTriangle, AlertCircle, Info } from 'lucide-react';

const AlertTable = ({ alerts }) => {
  const [sortField, setSortField] = useState('timestamp');
  const [sortDirection, setSortDirection] = useState('desc');
  const [expandedAlertId, setExpandedAlertId] = useState(null);
  
  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };
  
  const sortedAlerts = [...alerts].sort((a, b) => {
    if (sortField === 'timestamp') {
      return sortDirection === 'asc' 
        ? new Date(a.timestamp) - new Date(b.timestamp)
        : new Date(b.timestamp) - new Date(a.timestamp);
    } else {
      const aValue = a[sortField].toString().toLowerCase();
      const bValue = b[sortField].toString().toLowerCase();
      return sortDirection === 'asc'
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue);
    }
  });

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };
  
  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'Critical':
        return <AlertCircle size={16} className="text-red-500" />;
      case 'High':
        return <AlertTriangle size={16} className="text-orange-500" />;
      case 'Medium':
        return <AlertTriangle size={16} className="text-yellow-500" />;
      default:
        return <Info size={16} className="text-blue-500" />;
    }
  };
  
  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'Critical':
        return 'bg-red-100 text-red-800';
      case 'High':
        return 'bg-orange-100 text-orange-800';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-blue-100 text-blue-800';
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" onClick={() => handleSort('timestamp')}>
              <div className="flex items-center">
                Time
                {sortField === 'timestamp' && (
                  sortDirection === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />
                )}
              </div>
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" onClick={() => handleSort('type')}>
              <div className="flex items-center">
                Type
                {sortField === 'type' && (
                  sortDirection === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />
                )}
              </div>
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" onClick={() => handleSort('severity')}>
              <div className="flex items-center">
                Severity
                {sortField === 'severity' && (
                  sortDirection === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />
                )}
              </div>
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" onClick={() => handleSort('source')}>
              <div className="flex items-center">
                Source
                {sortField === 'source' && (
                  sortDirection === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />
                )}
              </div>
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {sortedAlerts.map((alert) => (
            <React.Fragment key={alert.id}>
              <tr className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {formatTimestamp(alert.timestamp)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {alert.type}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getSeverityClass(alert.severity)}`}>
                      {getSeverityIcon(alert.severity)} 
                      <span className="ml-1">{alert.severity}</span>
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {alert.source}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    onClick={() => setExpandedAlertId(expandedAlertId === alert.id ? null : alert.id)}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    {expandedAlertId === alert.id ? 'Hide Details' : 'View Details'}
                  </button>
                </td>
              </tr>
              {expandedAlertId === alert.id && (
                <tr className="bg-gray-50">
                  <td colSpan="5" className="px-6 py-4">
                    <div className="text-sm text-gray-700">
                      <div className="mb-2">
                        <span className="font-semibold">Destination:</span> {alert.destination}
                      </div>
                      <div>
                        <span className="font-semibold">Details:</span> {alert.details}
                      </div>
                      <div className="mt-4 flex space-x-2">
                        <button className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">
                          Investigate
                        </button>
                        <button className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700">
                          Block Source
                        </button>
                        <button className="px-3 py-1 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">
                          Dismiss
                        </button>
                      </div>
                    </div>
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AlertTable;