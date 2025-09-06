from flask import jsonify, request, send_file
from app.api import api_bp
from app.services.alpha_vantage import AlphaVantageService
from app.utils.vendor_analysis import VendorAnalyzer
import os
import tempfile

# Initialize services
alpha_vantage = AlphaVantageService()
analyzer = VendorAnalyzer()

# Vendor symbols
VENDOR_SYMBOLS = ['TEL', 'ST', 'DD', 'CE', 'LYB']

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Windborne Systems API is running'
    })

@api_bp.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint for basic functionality"""
    return jsonify({
        'message': 'Hello from Windborne Systems Backend!',
        'data': {
            'timestamp': '2024-01-01T00:00:00Z',
            'version': '1.0.0'
        }
    })

@api_bp.route('/vendors', methods=['GET'])
def get_vendors():
    """Get all vendor data"""
    try:
        vendors_data = alpha_vantage.get_all_vendors_data(VENDOR_SYMBOLS)
        analysis = analyzer.analyze_vendor_data(vendors_data)
        
        return jsonify({
            'success': True,
            'data': {
                'vendors': vendors_data,
                'analysis': analysis
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/vendors/<symbol>', methods=['GET'])
def get_vendor(symbol):
    """Get data for a specific vendor"""
    try:
        if symbol.upper() not in VENDOR_SYMBOLS:
            return jsonify({
                'success': False,
                'error': 'Invalid vendor symbol'
            }), 400
        
        vendor_data = alpha_vantage.get_vendor_data(symbol.upper())
        return jsonify({
            'success': True,
            'data': vendor_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/vendors/export/csv', methods=['GET'])
def export_vendors_csv():
    """Export vendor comparison data to CSV"""
    try:
        vendors_data = alpha_vantage.get_all_vendors_data(VENDOR_SYMBOLS)
        analysis = analyzer.analyze_vendor_data(vendors_data)
        
        # Create temporary CSV file
        temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False)
        filename = analyzer.export_to_csv(analysis['comparison_table'], temp_file.name)
        
        return send_file(
            filename,
            as_attachment=True,
            download_name='vendor_comparison.csv',
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/data', methods=['GET', 'POST'])
def handle_data():
    """Legacy endpoint - use /vendors instead"""
    return jsonify({
        'message': 'This endpoint is deprecated. Use /api/vendors for vendor data.',
        'available_endpoints': [
            '/api/vendors - Get all vendor data',
            '/api/vendors/<symbol> - Get specific vendor data',
            '/api/vendors/export/csv - Export vendor data as CSV'
        ]
    }), 410

@api_bp.route('/keys/status', methods=['GET'])
def get_key_status():
    """Get API key rotation status"""
    try:
        stats = alpha_vantage.key_manager.get_key_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/keys/reset', methods=['POST'])
def reset_key_blacklist():
    """Reset API key blacklist (for testing)"""
    try:
        alpha_vantage.key_manager.reset_blacklist()
        return jsonify({
            'success': True,
            'message': 'Key blacklist reset successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
