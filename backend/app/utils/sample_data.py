"""
Sample data for demonstration when Alpha Vantage API is rate limited
"""
from typing import Dict

def get_sample_vendor_data(symbol: str) -> Dict:
    """Get sample vendor data for demonstration purposes"""
    
    sample_data = {
        'TEL': {
            'overview': {
                'Name': 'TE Connectivity Ltd',
                'Symbol': 'TEL',
                'MarketCapitalization': '61619810000',
                'RevenueTTM': '16581000000',
                'PERatio': '42.39',
                'ReturnOnEquityTTM': '0.115',
                'DebtToEquity': '0.45',
                'CurrentRatio': '1.8',
                'DividendYield': '0.0129',
                'OperatingMarginTTM': '0.197',
                'ProfitMargin': '0.0877',
                'PriceToSalesRatioTTM': '3.72',
                'EVToEBITDA': '17.1'
            },
            'income_statement': {
                'annualReports': [{
                    'totalRevenue': '16581000000',
                    'grossProfit': '6500000000',
                    'operatingIncome': '3265000000',
                    'netIncome': '1452000000'
                }]
            }
        },
        'ST': {
            'overview': {
                'Name': 'Sensata Technologies Holding plc',
                'Symbol': 'ST',
                'MarketCapitalization': '4500000000',
                'RevenueTTM': '3800000000',
                'PERatio': '15.2',
                'ReturnOnEquityTTM': '0.08',
                'DebtToEquity': '0.65',
                'CurrentRatio': '2.1',
                'DividendYield': '0.0',
                'OperatingMarginTTM': '0.12',
                'ProfitMargin': '0.06',
                'PriceToSalesRatioTTM': '1.18',
                'EVToEBITDA': '8.5'
            },
            'income_statement': {
                'annualReports': [{
                    'totalRevenue': '3800000000',
                    'grossProfit': '1400000000',
                    'operatingIncome': '456000000',
                    'netIncome': '228000000'
                }]
            }
        },
        'DD': {
            'overview': {
                'Name': 'DuPont de Nemours Inc',
                'Symbol': 'DD',
                'MarketCapitalization': '12000000000',
                'RevenueTTM': '12000000000',
                'PERatio': '25.5',
                'ReturnOnEquityTTM': '0.15',
                'DebtToEquity': '0.35',
                'CurrentRatio': '2.5',
                'DividendYield': '0.02',
                'OperatingMarginTTM': '0.18',
                'ProfitMargin': '0.12',
                'PriceToSalesRatioTTM': '1.0',
                'EVToEBITDA': '12.5'
            },
            'income_statement': {
                'annualReports': [{
                    'totalRevenue': '12000000000',
                    'grossProfit': '4800000000',
                    'operatingIncome': '2160000000',
                    'netIncome': '1440000000'
                }]
            }
        },
        'CE': {
            'overview': {
                'Name': 'Celanese Corporation',
                'Symbol': 'CE',
                'MarketCapitalization': '8000000000',
                'RevenueTTM': '8500000000',
                'PERatio': '18.5',
                'ReturnOnEquityTTM': '0.22',
                'DebtToEquity': '0.55',
                'CurrentRatio': '1.9',
                'DividendYield': '0.025',
                'OperatingMarginTTM': '0.16',
                'ProfitMargin': '0.14',
                'PriceToSalesRatioTTM': '0.94',
                'EVToEBITDA': '9.8'
            },
            'income_statement': {
                'annualReports': [{
                    'totalRevenue': '8500000000',
                    'grossProfit': '2550000000',
                    'operatingIncome': '1360000000',
                    'netIncome': '1190000000'
                }]
            }
        },
        'LYB': {
            'overview': {
                'Name': 'LyondellBasell Industries N.V.',
                'Symbol': 'LYB',
                'MarketCapitalization': '35000000000',
                'RevenueTTM': '45000000000',
                'PERatio': '12.8',
                'ReturnOnEquityTTM': '0.28',
                'DebtToEquity': '0.75',
                'CurrentRatio': '1.6',
                'DividendYield': '0.045',
                'OperatingMarginTTM': '0.14',
                'ProfitMargin': '0.08',
                'PriceToSalesRatioTTM': '0.78',
                'EVToEBITDA': '6.2'
            },
            'income_statement': {
                'annualReports': [{
                    'totalRevenue': '45000000000',
                    'grossProfit': '9000000000',
                    'operatingIncome': '6300000000',
                    'netIncome': '3600000000'
                }]
            }
        }
    }
    
    return sample_data.get(symbol, {
        'overview': {
            'Name': 'Unknown Company',
            'Symbol': symbol,
            'MarketCapitalization': '0',
            'RevenueTTM': '0',
            'PERatio': '0',
            'ReturnOnEquityTTM': '0',
            'DebtToEquity': '0',
            'CurrentRatio': '0',
            'DividendYield': '0',
            'OperatingMarginTTM': '0',
            'ProfitMargin': '0',
            'PriceToSalesRatioTTM': '0',
            'EVToEBITDA': '0'
        },
        'income_statement': {
            'annualReports': []
        }
    })
