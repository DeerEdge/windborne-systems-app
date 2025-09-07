import React from 'react';
import { AlertTriangle, TrendingUp, TrendingDown, Minus, Download } from 'lucide-react';

const VendorTable = ({ analysis }) => {
  const { comparison_table, flags } = analysis;

  const getFlagIcon = (flagString) => {
    if (!flagString || flagString === 'None') return null;
    
    const flagList = flagString.split(', ');
    const hasWarnings = flagList.some(flag => 
      ['LOW_REVENUE', 'HIGH_PE', 'HIGH_DEBT', 'LOW_LIQUIDITY', 'LOW_ROE'].includes(flag)
    );
    
    return hasWarnings ? (
      <AlertTriangle className="w-4 h-4 text-red-500" />
    ) : null;
  };

  const getFlagTooltip = (flagString) => {
    if (!flagString || flagString === 'None') return '';
    
    const flagMap = {
      'LOW_REVENUE': 'Low Revenue (< $1B)',
      'HIGH_PE': 'High P/E Ratio (> 30)',
      'HIGH_DEBT': 'High Debt-to-Equity (> 1.0)',
      'LOW_LIQUIDITY': 'Low Current Ratio (< 1.0)',
      'LOW_ROE': 'Low ROE (< 10%)',
      'LOW_OPERATING_MARGIN': 'Low Operating Margin (< 5%)',
      'LOW_PROFIT_MARGIN': 'Low Profit Margin (< 3%)',
      'HIGH_PRICE_TO_SALES': 'High Price/Sales (> 10)',
      'HIGH_EV_TO_EBITDA': 'High EV/EBITDA (> 20)',
      'API_ERROR': 'API Error'
    };
    
    return flagString.split(', ').map(flag => flagMap[flag] || flag).join(', ');
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'Sensors':
        return 'bg-blue-100/80 text-blue-700';
      case 'Plastics/Materials':
        return 'bg-emerald-100/80 text-emerald-700';
      default:
        return 'bg-slate-100/80 text-slate-700';
    }
  };

  const formatNumber = (value, decimals = 2) => {
    if (value === null || value === undefined || isNaN(value)) return 'N/A';
    return Number(value).toFixed(decimals);
  };

  const exportVendorData = (vendor) => {
    // Create CSV content for individual vendor
    const csvContent = [
      ['Metric', 'Value'],
      ['Company Name', vendor.Name],
      ['Symbol', vendor.Symbol],
      ['Category', vendor.Category],
      ['Market Cap ($B)', formatNumber(vendor['Market Cap ($B)'])],
      ['Revenue ($B)', formatNumber(vendor['Revenue ($B)'])],
      ['P/E Ratio', formatNumber(vendor['P/E Ratio'])],
      ['ROE (%)', formatNumber(vendor['ROE (%)'])],
      ['Debt/Equity', formatNumber(vendor['Debt/Equity'])],
      ['Current Ratio', formatNumber(vendor['Current Ratio'])],
      ['Dividend Yield (%)', formatNumber(vendor['Dividend Yield (%)'])],
      ['Operating Margin (%)', formatNumber(vendor['Operating Margin (%)'])],
      ['Profit Margin (%)', formatNumber(vendor['Profit Margin (%)'])],
      ['Price/Sales', formatNumber(vendor['Price/Sales'])],
      ['EV/EBITDA', formatNumber(vendor['EV/EBITDA'])],
      ['Flags', vendor.Flags || 'None']
    ].map(row => row.join(',')).join('\n');

    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `${vendor.Symbol}_${vendor.Name.replace(/\s+/g, '_')}_statistics.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="overflow-hidden">
      <div className="px-8 py-6 border-b border-slate-100 bg-slate-50">
        <h3 className="text-2xl font-light text-slate-800 mb-2">Vendor Comparison</h3>
        <p className="text-slate-500">
          Financial metrics and analysis for potential vendors
        </p>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-100">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-4 text-center text-xs font-semibold text-slate-600 uppercase tracking-wider w-16">
              </th>
              <th className="px-8 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Vendor
              </th>
              <th className="px-8 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Category
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Market Cap ($B)
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Revenue ($B)
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                P/E Ratio
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                ROE (%)
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Debt/Equity
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Current Ratio
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Dividend Yield (%)
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Operating Margin (%)
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Profit Margin (%)
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Price/Sales
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider">
                EV/EBITDA
              </th>
              <th className="px-6 py-4 text-center text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Flags
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-100">
            {comparison_table.map((vendor, index) => (
              <tr key={vendor.Symbol} className={index % 2 === 0 ? 'bg-white' : 'bg-slate-50 hover:bg-slate-100 transition-colors duration-150'}>
                <td className="px-6 py-6 whitespace-nowrap text-center">
                  <button
                    onClick={() => exportVendorData(vendor)}
                    className="inline-flex items-center justify-center w-8 h-8 border border-slate-200 rounded-md text-slate-600 bg-white hover:bg-slate-50 hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-300 transition-all duration-200"
                    title={`Export ${vendor.Name} statistics`}
                  >
                    <Download className="w-4 h-4" />
                  </button>
                </td>
                <td className="px-8 py-6 whitespace-nowrap">
                  <div className="flex items-center">
                    <div>
                      <div className="text-base font-medium text-slate-800">
                        {vendor.Name}
                      </div>
                      <div className="text-sm text-slate-500">
                        {vendor.Symbol}
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-8 py-6 whitespace-nowrap">
                  <span className={`inline-flex px-3 py-1.5 text-xs font-semibold rounded-full ${getCategoryColor(vendor.Category)}`}>
                    {vendor.Category}
                  </span>
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['Market Cap ($B)'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['Revenue ($B)'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['P/E Ratio'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['ROE (%)'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['Debt/Equity'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['Current Ratio'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['Dividend Yield (%)'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['Operating Margin (%)'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['Profit Margin (%)'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['Price/Sales'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-right text-sm text-slate-700 font-medium">
                  {formatNumber(vendor['EV/EBITDA'])}
                </td>
                <td className="px-6 py-6 whitespace-nowrap text-center">
                  <div 
                    className="inline-flex items-center"
                    title={getFlagTooltip(vendor.Flags)}
                  >
                    {getFlagIcon(vendor.Flags)}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="px-8 py-4 bg-slate-50 border-t border-slate-100">
        <div className="flex items-center justify-between text-sm text-slate-500">
          <div className="flex items-center">
            <AlertTriangle className="w-4 h-4 mr-2 text-amber-500" />
            <span>Flags indicate potential concerns</span>
          </div>
          <div className="font-medium">
            {comparison_table.length} vendors analyzed
          </div>
        </div>
      </div>
    </div>
  );
};

export default VendorTable;
