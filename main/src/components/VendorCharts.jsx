import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from 'recharts';

const VendorCharts = ({ analysis }) => {
  const { comparison_table } = analysis;

  // Prepare data for revenue comparison chart
  const revenueData = comparison_table
    .filter(vendor => vendor['Revenue ($B)'] > 0)
    .map(vendor => ({
      name: vendor.Symbol,
      revenue: vendor['Revenue ($B)'],
      category: vendor.Category
    }))
    .sort((a, b) => b.revenue - a.revenue);

  // Prepare data for P/E ratio comparison
  const peData = comparison_table
    .filter(vendor => vendor['P/E Ratio'] > 0)
    .map(vendor => ({
      name: vendor.Symbol,
      peRatio: vendor['P/E Ratio'],
      category: vendor.Category
    }))
    .sort((a, b) => b.peRatio - a.peRatio);

  // Prepare data for ROE comparison
  const roeData = comparison_table
    .filter(vendor => vendor['ROE (%)'] > 0)
    .map(vendor => ({
      name: vendor.Symbol,
      roe: vendor['ROE (%)'],
      category: vendor.Category
    }))
    .sort((a, b) => b.roe - a.roe);

  // Prepare data for category distribution pie chart
  const categoryData = comparison_table.reduce((acc, vendor) => {
    const category = vendor.Category;
    const existing = acc.find(item => item.name === category);
    if (existing) {
      existing.value += 1;
    } else {
      acc.push({ name: category, value: 1 });
    }
    return acc;
  }, []);

  const colors = {
    'Sensors': '#60A5FA',
    'Plastics/Materials': '#34D399',
    'Unknown': '#94A3B8'
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white/95 backdrop-blur-sm p-4 border border-slate-200 rounded-xl shadow-xl">
          <p className="font-medium text-slate-800 mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="text-sm text-slate-600" style={{ color: entry.color }}>
              {entry.dataKey}: {entry.value}
              {entry.dataKey === 'revenue' && 'B'}
              {entry.dataKey === 'peRatio' && ''}
              {entry.dataKey === 'roe' && '%'}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Revenue Comparison */}
      <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg border border-slate-100">
        <h3 className="text-xl font-light text-slate-800 mb-6">Revenue Comparison ($B)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={revenueData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip content={<CustomTooltip />} />
            <Bar 
              dataKey="revenue" 
              fill="#60A5FA"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* P/E Ratio Comparison */}
      <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg border border-slate-100">
        <h3 className="text-xl font-light text-slate-800 mb-6">P/E Ratio Comparison</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={peData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip content={<CustomTooltip />} />
            <Bar 
              dataKey="peRatio" 
              fill="#34D399"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* ROE Comparison */}
      <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg border border-slate-100">
        <h3 className="text-xl font-light text-slate-800 mb-6">Return on Equity (%)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={roeData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip content={<CustomTooltip />} />
            <Bar 
              dataKey="roe" 
              fill="#FBBF24"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Category Distribution */}
      <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg border border-slate-100">
        <h3 className="text-xl font-light text-slate-800 mb-6">Vendor Categories</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={categoryData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {categoryData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={colors[entry.name] || '#6B7280'} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default VendorCharts;
