from flask import Flask, render_template, request, send_file, session, jsonify
from generate_chart import generate_chart_buffer
import base64
import io
import os
import sys
import yfinance as yf
from contextlib import contextmanager

@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    try:
        fnull = open(os.devnull, 'w')
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = fnull
        sys.stderr = fnull
    except Exception:
        # If setup fails, just yield and do nothing
        yield
        return

    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        fnull.close()

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_chart():
    try:
        print("Received /generate request")
        print("Form Data:", request.form)
        
        # Basic Validation
        ticker = request.form.get('ticker')
        if not ticker:
            print("Error: Ticker is missing")
            return jsonify({'error': 'Ticker is required'}), 400
        
        period = request.form.get('period')
        interval = request.form.get('interval')
        resolution = request.form.get('resolution')
        style = request.form.get('style')
        title = request.form.get('title')
        chart_type = request.form.get('chart_type', 'line')
        
        
        # Optional start/end dates
        start = request.form.get('start')
        end = request.form.get('end')
        if not start: start = None
        if not end: end = None
        
        # Optional comparison
        compare_ticker = request.form.get('compare_ticker')
        if compare_ticker:
            if ',' in compare_ticker:
                compare_ticker = [t.strip() for t in compare_ticker.split(',')]
            else:
                compare_ticker = compare_ticker.strip()
        else:
            compare_ticker = None

        # Customization
        primary_color = request.form.get('primary_color')
        primary_type = request.form.get('primary_type', 'line')
        compare_color = request.form.get('compare_color')
        compare_type = request.form.get('compare_type', 'line')
        bg_color = request.form.get('bg_color', 'transparent')
        
        # Advanced Customization
        try:
            grid_opacity = float(request.form.get('grid_opacity', 10.0)) / 100.0
        except ValueError:
            grid_opacity = 0.1
        
        # Per-Asset Settings (new feature)
        per_asset_settings = None
        per_asset_settings_json = request.form.get('per_asset_settings')
        if per_asset_settings_json:
            try:
                import json
                per_asset_settings = json.loads(per_asset_settings_json)
                print(f"Per-asset settings: {per_asset_settings}")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing per-asset settings: {e}")
                per_asset_settings = None
        
        # Output Format (PNG or SVG)
        output_format = request.form.get('output_format', 'png').lower()
        if output_format not in ['png', 'svg']:
            output_format = 'png'
        print(f"Output format: {output_format}")

        # If chart_type is passed (legacy), it overrides primary_type if primary_type is default? 
        # Actually, let's use primary_type as the source of truth if present.
        # The form will send chart_type as 'candle' or 'line' from the old toggle. 
        # We should unify this. Let's assume the new UI sends primary_type.
        # But for backward compatibility or if we keep the old toggle, we need to be careful.
        # Let's map chart_type to primary_type if primary_type is not explicitly set?
        # Or just use chart_type as primary_type.
        
        # Let's use the 'chart_type' field from the form as 'primary_type' since that's what the old toggle uses.
        # But the new UI might send 'primary_type'.
        # Let's prefer 'primary_type' if available, else 'chart_type'.
        
        final_primary_type = primary_type if primary_type else chart_type

        # with suppress_stdout_stderr():
        buf = generate_chart_buffer(
            ticker, period, interval, start, end, resolution, style, title, 
            chart_type=final_primary_type, 
            compare_ticker=compare_ticker,
            primary_color=primary_color,
            compare_color=compare_color,
            compare_type=compare_type,
            bg_color=bg_color,
            grid_opacity=grid_opacity,
            per_asset_settings=per_asset_settings,
            output_format=output_format
        )
        
        # Store image data, ticker, and format in session for download
        img_bytes = buf.getvalue()
        session['chart_image'] = base64.b64encode(img_bytes).decode('utf-8')
        session['chart_ticker'] = ticker
        session['chart_format'] = output_format
        
        # Return base64 for display with format info
        return {'image': session['chart_image'], 'ticker': ticker, 'format': output_format}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error generating chart: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/economic-data', methods=['GET'])
def economic_data():
    try:
        from economic_data import get_economic_data
        data = get_economic_data()
        return data
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/ticker-data/<ticker>', methods=['GET'])
def ticker_data(ticker):
    """Get current ticker price and time"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period='5d')
        
        if hist.empty:
            return jsonify({"error": "No data available"}), 404
        
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change_pct = ((current_price - prev_close) / prev_close) * 100
        
        return jsonify({
            "ticker": ticker,
            "price": f"{current_price:.2f}",
            "currency": info.get('currency', 'USD'),
            "change_pct": change_pct,
            "time": datetime.now().strftime("%H:%M")
        })
    except Exception as e:
        print(f"Error fetching ticker data: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/asset-insights/<ticker>')
def asset_insights(ticker):
    """Get comprehensive financial insights for an asset"""
    try:
        from asset_insights import get_asset_insights
        insights = get_asset_insights(ticker)
        return jsonify(insights)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/news/<country>', methods=['GET'])
def get_news_api(country):
    """Get analyzed news for a country"""
    try:
        from news_data import get_news
        news = get_news(country)
        return jsonify(news)
    except Exception as e:
        print(f"Error in news API: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        # Get image data, ticker, and format from POST request
        data = request.get_json()
        img_base64 = data.get('image')
        ticker = data.get('ticker', 'chart')
        file_format = data.get('format', 'png').lower()
        
        if not img_base64:
            return {'error': 'No image data provided'}, 400
        
        # Decode base64 to bytes
        img_bytes = base64.b64decode(img_base64)
        buf = io.BytesIO(img_bytes)
        buf.seek(0)
        
        # Determine MIME type and file extension
        if file_format == 'svg':
            mimetype = 'image/svg+xml'
            extension = 'svg'
        else:
            mimetype = 'image/png'
            extension = 'png'
        
        # Send file with proper headers
        return send_file(
            buf,
            mimetype=mimetype,
            as_attachment=True,
            download_name=f'{ticker}_chart.{extension}'
        )
        
    except Exception as e:
        return {'error': str(e)}, 400

# --- Templates & History API ---
from storage import TemplateManager, HistoryManager

template_manager = TemplateManager()
history_manager = HistoryManager()

@app.route('/api/templates', methods=['GET'])
def get_templates():
    return jsonify(template_manager.get_templates())

@app.route('/api/templates', methods=['POST'])
def save_template():
    data = request.json
    name = data.get('name')
    config = data.get('config')
    if not name or not config:
        return jsonify({'error': 'Name and config required'}), 400
    
    template_manager.save_template(name, config)
    return jsonify({'success': True})

@app.route('/api/templates/<name>', methods=['DELETE'])
def delete_template(name):
    if template_manager.delete_template(name):
        return jsonify({'success': True})
    return jsonify({'error': 'Template not found'}), 404

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(history_manager.get_history())

@app.route('/api/history', methods=['POST'])
def add_history():
    data = request.json
    history_manager.add_history(data)
    return jsonify({'success': True})

@app.route('/api/history/<int:index>', methods=['DELETE'])
def delete_history_item(index):
    if history_manager.delete_history(index):
        return jsonify({'success': True})
    return jsonify({'error': 'History item not found'}), 404

@app.route('/api/history/clear', methods=['DELETE'])
def clear_all_history():
    history_manager.clear_all_history()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    # Trigger reload (Fixed US Index/Currency Data)
