#!/usr/bin/env python3
"""
Simplified Web Server for Law Firm Review Tracking Dashboard
Works with demo data initially - can be connected to real database later
"""

from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Demo data generator
def generate_demo_data():
    """Generate realistic demo data"""
    base_reviews = 48532
    base_rating = 4.3
    
    # Add some randomness
    daily_change = random.randint(-50, 250)
    rating_change = random.uniform(-0.2, 0.1)
    
    return {
        'metrics': {
            'total_locations': 120,
            'total_reviews': base_reviews + daily_change,
            'average_rating': round(base_rating + rating_change, 2),
            'reviews_removed_today': random.randint(0, 30),
            'reviews_added_24h': random.randint(100, 300),
            'change_7d_reviews': random.randint(800, 1500),
            'change_7d_rating': round(random.uniform(-0.3, 0.2), 2)
        }
    }

@app.route('/')
def home():
    """Home endpoint"""
    return '''
    <h1>Law Firm Review Tracking API</h1>
    <p>Dashboard API is running!</p>
    <p>Connect your dashboard to: <code>https://[this-server-url]</code></p>
    <br>
    <h3>Available Endpoints:</h3>
    <ul>
        <li><a href="/api/metrics">/api/metrics</a> - Current metrics</li>
        <li><a href="/api/trends/7d">/api/trends/7d</a> - 7-day trends</li>
        <li><a href="/api/locations/top">/api/locations/top</a> - Top locations</li>
        <li><a href="/api/locations/attention">/api/locations/attention</a> - Locations needing attention</li>
        <li><a href="/api/rating-distribution">/api/rating-distribution</a> - Rating distribution</li>
    </ul>
    '''

@app.route('/api/metrics')
def get_metrics():
    """Get current metrics for dashboard"""
    data = generate_demo_data()
    return jsonify(data['metrics'])

@app.route('/api/trends/<period>')
def get_trends(period):
    """Get trend data for specified period"""
    days = {
        '24h': 1,
        '7d': 7,
        '30d': 30,
        '90d': 90
    }.get(period, 7)
    
    trends = []
    today = datetime.now()
    
    for i in range(days):
        date = today - timedelta(days=days-i-1)
        trends.append({
            'date': date.strftime('%b %d'),
            'reviews_added': random.randint(30, 80),
            'reviews_removed': random.randint(0, 10),
            'average_rating': round(4.3 + random.uniform(-0.2, 0.2), 2)
        })
    
    return jsonify(trends)

@app.route('/api/locations/top')
def get_top_locations():
    """Get top performing locations"""
    cities = [
        ('Miami Downtown', 'Miami', 4.8, 1245),
        ('Orlando Central', 'Orlando', 4.7, 892),
        ('Tampa Bay', 'Tampa', 4.6, 756),
        ('Jacksonville North', 'Jacksonville', 4.5, 623),
        ('Fort Lauderdale', 'Fort Lauderdale', 4.5, 589),
        ('West Palm Beach', 'West Palm Beach', 4.4, 456),
        ('Tallahassee Main', 'Tallahassee', 4.4, 412),
        ('Gainesville', 'Gainesville', 4.3, 389),
        ('Naples', 'Naples', 4.3, 356),
        ('Sarasota', 'Sarasota', 4.2, 298)
    ]
    
    locations = []
    for name, city, rating, reviews in cities[:10]:
        change = random.randint(-5, 20)
        status = 'Excellent' if rating >= 4.5 else 'Good' if rating >= 4.0 else 'Monitor'
        locations.append({
            'name': f'Law Firm - {name}',
            'city': f'{city}, FL',
            'rating': rating,
            'total_reviews': reviews,
            'change': change,
            'status': status
        })
    
    return jsonify(locations)

@app.route('/api/locations/attention')
def get_attention_locations():
    """Get locations needing attention"""
    problem_locations = [
        ('Lakeland Branch', 'Lakeland', 3.2, 8, 'Multiple Reviews Removed'),
        ('Coral Gables', 'Coral Gables', 3.5, 3, 'Rating Drop'),
        ('Fort Myers', 'Fort Myers', 3.4, 2, 'Low Rating'),
        ('Clearwater', 'Clearwater', 3.6, 4, 'Reviews Removed'),
        ('Ocala', 'Ocala', 3.3, 1, 'Low Rating')
    ]
    
    locations = []
    for name, city, rating, removed, issue in problem_locations:
        priority = 'Urgent' if removed > 5 or rating < 3.3 else 'High' if rating < 3.5 else 'Medium'
        locations.append({
            'name': f'Law Firm - {name}',
            'city': city,
            'issue': issue,
            'rating': rating,
            'reviews_removed': removed,
            'priority': priority
        })
    
    return jsonify(locations)

@app.route('/api/rating-distribution')
def get_rating_distribution():
    """Get star rating distribution"""
    total = 48532
    distribution = {
        '5_star': int(total * 0.45),  # 45% 5-star
        '4_star': int(total * 0.30),  # 30% 4-star
        '3_star': int(total * 0.15),  # 15% 3-star
        '2_star': int(total * 0.07),  # 7% 2-star
        '1_star': int(total * 0.03)   # 3% 1-star
    }
    
    return jsonify(distribution)

@app.route('/api/alerts/recent')
def get_recent_alerts():
    """Get recent alerts"""
    if random.random() > 0.7:  # 30% chance of having alerts
        return jsonify([{
            'date': datetime.now().isoformat(),
            'location': 'Law Firm - Lakeland Branch',
            'type': 'reviews_removed',
            'message': '8 reviews removed in the last 24 hours'
        }])
    return jsonify([])

@app.route('/api/export/excel')
def export_excel():
    """Trigger Excel report generation"""
    return jsonify({
        'success': True,
        'message': 'Report generation simulated',
        'filename': f'review_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)