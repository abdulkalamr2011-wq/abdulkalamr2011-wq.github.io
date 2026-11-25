"""Saveetha Bus Alert: a small Flask demo for departure estimates.

The presentation does not include training data or a trained model. This demo
therefore uses a transparent, configurable heuristic and labels all values as
sample estimates. Replace predict_delay() with a trained model when trip data
is available.
"""

from datetime import datetime, timedelta
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "bus-alert-demo-local"

TRIPS = [
    {"bus": "Bus 07", "route": "Tambaram · Main Gate", "scheduled": "08:15", "delay": 8, "status": "Delayed", "updated": "Just now"},
    {"bus": "Bus 12", "route": "Velachery · Main Gate", "scheduled": "08:30", "delay": 2, "status": "On time", "updated": "3 min ago"},
    {"bus": "Bus 03", "route": "Avadi · Main Gate", "scheduled": "08:45", "delay": 14, "status": "Delayed", "updated": "5 min ago"},
]


def predict_delay(traffic, weather, gps_progress, history):
    """Return an illustrative delay in minutes, not a production ML output."""
    traffic_points = {"Light": 0, "Moderate": 4, "Heavy": 10}[traffic]
    weather_points = {"Clear": 0, "Rain": 5}[weather]
    # Approximate progress reduces uncertainty as a bus approaches its stop.
    progress_adjustment = 3 if gps_progress < 25 else (1 if gps_progress < 60 else 0)
    return max(0, round(traffic_points + weather_points + progress_adjustment + history))


@app.get("/")
def dashboard():
    return render_template("index.html", trips=TRIPS, result=None, now=datetime.now().strftime("%A, %d %b"))


@app.post("/predict")
def predict():
    bus = request.form.get("bus", "Bus 07").strip() or "Bus 07"
    route = request.form.get("route", "Tambaram · Main Gate").strip() or "Route not set"
    scheduled = request.form.get("scheduled", "08:15")
    traffic = request.form.get("traffic", "Moderate")
    weather = request.form.get("weather", "Clear")
    try:
        progress = min(100, max(0, int(request.form.get("progress", 55))))
        history = min(30, max(0, int(request.form.get("history", 2))))
        departure = datetime.strptime(scheduled, "%H:%M")
    except (ValueError, TypeError):
        flash("Enter a valid time and numeric values for GPS progress and typical delay.", "error")
        return redirect(url_for("dashboard"))
    if traffic not in {"Light", "Moderate", "Heavy"} or weather not in {"Clear", "Rain"}:
        flash("Choose a listed traffic and weather option.", "error")
        return redirect(url_for("dashboard"))

    delay = predict_delay(traffic, weather, progress, history)
    predicted = departure + timedelta(minutes=delay)
    status = "Alert recommended" if delay >= 5 else "Near schedule"
    result = {"bus": bus, "route": route, "scheduled": departure.strftime("%I:%M %p"),
              "predicted": predicted.strftime("%I:%M %p"), "delay": delay,
              "status": status, "traffic": traffic, "weather": weather, "progress": progress}
    TRIPS.insert(0, {"bus": bus, "route": route, "scheduled": departure.strftime("%H:%M"),
                     "delay": delay, "status": "Delayed" if delay >= 5 else "On time", "updated": "Just now"})
    del TRIPS[8:]
    return render_template("index.html", trips=TRIPS, result=result, now=datetime.now().strftime("%A, %d %b"))


if __name__ == "__main__":
    app.run(debug=True)

