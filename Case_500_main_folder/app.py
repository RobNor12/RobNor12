from flask import Flask, render_template, request, send_from_directory
from analysis import load_data, trend_report, normalize_report, rolling_correlation_report
from plotting import generate_plot

app = Flask(__name__)

# Pre-load data at startup to avoid re-reading CSVs on every page refresh
df = load_data()

@app.route("/", methods=["GET"])
def index():
    """Main route handling the dashboard logic and view switching."""
    view = request.args.get("view", "trends")

    if view == "normalized":
        data = normalize_report(df)
        title, filename = "Normalized Growth", "normalized.png"
    elif view == "correlation":
        data = rolling_correlation_report(df)
        title, filename = "12-Month Rolling Correlation", "correlation.png"
    else:
        data = trend_report(df)
        title, filename = "Market Trends", "trends.png"

    generate_plot(data, title, filename) 
    
    return render_template("index.html", plot=filename)

@app.route('/static_plots/<path:filename>')
def serve_plots(filename):
    """Custom route to serve images from the non-standard static_plots folder."""
    return send_from_directory('static_plots', filename)

if __name__ == "__main__":
    app.run(debug=True)

