import csv
from typing import Dict, List, Any
from datetime import datetime

class VendorAnalyzer:
    def __init__(self):
        self.vendor_categories = {
            'Sensors': ['TEL', 'ST'],
            'Plastics/Materials': ['DD', 'CE', 'LYB']
        }
    
    def analyze_vendor_data(self, vendors_data: Dict) -> Dict:
        """Analyze vendor data and generate insights"""
        analysis = {
            'summary': {},
            'comparison_table': [],
            'flags': {},
            'insights': []
        }
        
        for symbol, data in vendors_data.items():
            if 'error' in data:
                analysis['flags'][symbol] = ['API_ERROR']
                continue
            
            vendor_analysis = self._analyze_single_vendor(symbol, data)
            analysis['summary'][symbol] = vendor_analysis['summary']
            analysis['comparison_table'].append(vendor_analysis['row'])
            analysis['flags'][symbol] = vendor_analysis['flags']
        
        # Generate comparative insights
        analysis['insights'] = self._generate_insights(analysis['comparison_table'])
        
        return analysis
    
    def _analyze_single_vendor(self, symbol: str, data: Dict) -> Dict:
        """Analyze a single vendor's data"""
        overview = data.get('overview', {})
        
        # Extract key metrics from OVERVIEW endpoint
        name = overview.get('Name', 'Unknown')
        market_cap = self._safe_float(overview.get('MarketCapitalization', '0'))
        pe_ratio = self._safe_float(overview.get('PERatio', '0'))
        peg_ratio = self._safe_float(overview.get('PEGRatio', '0'))
        dividend_yield = self._safe_float(overview.get('DividendYield', '0'))
        roe = self._safe_float(overview.get('ReturnOnEquityTTM', '0'))
        roa = self._safe_float(overview.get('ReturnOnAssetsTTM', '0'))
        debt_to_equity = self._safe_float(overview.get('DebtToEquity', '0'))
        current_ratio = self._safe_float(overview.get('CurrentRatio', '0'))
        
        # Get revenue from overview (RevenueTTM)
        revenue = self._safe_float(overview.get('RevenueTTM', '0'))
        
        # Get additional metrics from overview
        total_debt = self._safe_float(overview.get('TotalDebt', '0'))
        gross_profit_ttm = self._safe_float(overview.get('GrossProfitTTM', '0'))
        operating_margin = self._safe_float(overview.get('OperatingMarginTTM', '0'))
        profit_margin = self._safe_float(overview.get('ProfitMargin', '0'))
        price_to_sales = self._safe_float(overview.get('PriceToSalesRatioTTM', '0'))
        price_to_book = self._safe_float(overview.get('PriceToBookRatio', '0'))
        ev_to_revenue = self._safe_float(overview.get('EVToRevenue', '0'))
        ev_to_ebitda = self._safe_float(overview.get('EVToEBITDA', '0'))
        
        # Calculate flags
        flags = []
        if revenue < 1000000000:  # Less than $1B
            flags.append('LOW_REVENUE')
        if pe_ratio > 30:
            flags.append('HIGH_PE')
        if debt_to_equity > 1.0:
            flags.append('HIGH_DEBT')
        if current_ratio < 1.0:
            flags.append('LOW_LIQUIDITY')
        if roe < 0.1:
            flags.append('LOW_ROE')
        if operating_margin < 0.05:  # Less than 5%
            flags.append('LOW_OPERATING_MARGIN')
        if profit_margin < 0.03:  # Less than 3%
            flags.append('LOW_PROFIT_MARGIN')
        if price_to_sales > 10:
            flags.append('HIGH_PRICE_TO_SALES')
        if ev_to_ebitda > 20:
            flags.append('HIGH_EV_TO_EBITDA')
        
        # Determine category
        category = 'Unknown'
        for cat, symbols in self.vendor_categories.items():
            if symbol in symbols:
                category = cat
                break
        
        summary = {
            'name': name,
            'symbol': symbol,
            'category': category,
            'market_cap': market_cap,
            'revenue': revenue,
            'pe_ratio': pe_ratio,
            'roe': roe,
            'debt_to_equity': debt_to_equity,
            'current_ratio': current_ratio,
            'dividend_yield': dividend_yield,
            'operating_margin': operating_margin,
            'profit_margin': profit_margin,
            'price_to_sales': price_to_sales,
            'ev_to_ebitda': ev_to_ebitda
        }
        
        row = {
            'Symbol': symbol,
            'Name': name,
            'Category': category,
            'Market Cap ($B)': round(market_cap / 1e9, 2),
            'Revenue ($B)': round(revenue / 1e9, 2),
            'P/E Ratio': round(pe_ratio, 2),
            'ROE (%)': round(roe * 100, 2),
            'Debt/Equity': round(debt_to_equity, 2),
            'Current Ratio': round(current_ratio, 2),
            'Dividend Yield (%)': round(dividend_yield * 100, 2),
            'Operating Margin (%)': round(operating_margin * 100, 2),
            'Profit Margin (%)': round(profit_margin * 100, 2),
            'Price/Sales': round(price_to_sales, 2),
            'EV/EBITDA': round(ev_to_ebitda, 2),
            'Flags': ', '.join(flags) if flags else 'None'
        }
        
        return {
            'summary': summary,
            'row': row,
            'flags': flags
        }
    
    def _safe_float(self, value: str) -> float:
        """Safely convert string to float"""
        if not value or value == 'None' or value == '-':
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    
    def _generate_insights(self, comparison_table: List[Dict]) -> List[str]:
        """Generate insights from comparison data"""
        insights = []
        
        if not comparison_table:
            return insights
        
        # Find highest revenue
        max_revenue = max(row['Revenue ($B)'] for row in comparison_table)
        max_revenue_vendor = next(row for row in comparison_table if row['Revenue ($B)'] == max_revenue)
        insights.append(f"Highest revenue: {max_revenue_vendor['Name']} ({max_revenue_vendor['Symbol']}) with ${max_revenue}B")
        
        # Find lowest P/E ratio
        valid_pe = [row for row in comparison_table if row['P/E Ratio'] > 0]
        if valid_pe:
            min_pe = min(row['P/E Ratio'] for row in valid_pe)
            min_pe_vendor = next(row for row in valid_pe if row['P/E Ratio'] == min_pe)
            insights.append(f"Most undervalued (lowest P/E): {min_pe_vendor['Name']} ({min_pe_vendor['Symbol']}) with P/E of {min_pe}")
        
        # Find highest ROE
        valid_roe = [row for row in comparison_table if row['ROE (%)'] > 0]
        if valid_roe:
            max_roe = max(row['ROE (%)'] for row in valid_roe)
            max_roe_vendor = next(row for row in valid_roe if row['ROE (%)'] == max_roe)
            insights.append(f"Highest ROE: {max_roe_vendor['Name']} ({max_roe_vendor['Symbol']}) with {max_roe}%")
        
        # Count flags
        flagged_vendors = [row for row in comparison_table if row['Flags'] != 'None']
        if flagged_vendors:
            insights.append(f"{len(flagged_vendors)} vendors have warning flags")
        
        return insights
    
    def export_to_csv(self, comparison_table: List[Dict], filename: str = None) -> str:
        """Export comparison table to CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vendor_comparison_{timestamp}.csv"
        
        # Write CSV using built-in csv module
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if comparison_table:
                fieldnames = comparison_table[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(comparison_table)
        
        return filename
