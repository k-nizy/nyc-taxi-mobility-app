"""
Flask REST API for NYC Taxi Trip Data
Provides endpoints for querying, filtering, and aggregating trip data
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import func, and_, or_, extract, desc
from datetime import datetime, timedelta
from models import get_session, Trip, Zone, PaymentType, RateCode
from algorithms import (
    QuickSort, MultiCriteriaFilter, TripGrouper, 
    AnomalyDetector, TopKSelector
)
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


def build_trip_filters(args):
    filters = []

    value = args.get('start_date')
    if value:
        try:
            start_date = datetime.strptime(value, '%Y-%m-%d')
            filters.append(Trip.pickup_datetime >= start_date)
        except ValueError:
            pass

    value = args.get('end_date')
    if value:
        try:
            end_date = datetime.strptime(value, '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)
            filters.append(Trip.pickup_datetime <= end_date)
        except ValueError:
            pass

    value = args.get('min_fare')
    if value not in (None, ''):
        try:
            filters.append(Trip.fare_amount >= float(value))
        except ValueError:
            pass

    value = args.get('max_fare')
    if value not in (None, ''):
        try:
            filters.append(Trip.fare_amount <= float(value))
        except ValueError:
            pass

    value = args.get('min_distance')
    if value not in (None, ''):
        try:
            filters.append(Trip.trip_distance >= float(value))
        except ValueError:
            pass

    value = args.get('max_distance')
    if value not in (None, ''):
        try:
            filters.append(Trip.trip_distance <= float(value))
        except ValueError:
            pass

    value = args.get('pickup_zone_id')
    if value not in (None, ''):
        try:
            filters.append(Trip.pickup_zone_id == int(value))
        except ValueError:
            pass

    value = args.get('dropoff_zone_id')
    if value not in (None, ''):
        try:
            filters.append(Trip.dropoff_zone_id == int(value))
        except ValueError:
            pass

    value = args.get('passenger_count')
    if value not in (None, ''):
        try:
            filters.append(Trip.passenger_count == int(value))
        except ValueError:
            pass

    return filters


@app.route('/')
def index():
    """API information endpoint."""
    return jsonify({
        'name': 'NYC Taxi Mobility Analytics API',
        'version': '1.0.0',
        'endpoints': {
            'trips': '/api/trips',
            'statistics': '/api/statistics',
            'zones': '/api/zones',
            'time_series': '/api/time-series',
            'heatmap': '/api/heatmap',
            'anomalies': '/api/anomalies',
            'top_routes': '/api/top-routes'
        }
    })


@app.route('/api/trips', methods=['GET'])
def get_trips():
    """
    Retrieve trips with optional filters.
    
    Query Parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - min_fare: Minimum fare amount
    - max_fare: Maximum fare amount
    - min_distance: Minimum trip distance
    - max_distance: Maximum trip distance
    - pickup_zone_id: Pickup zone ID
    - dropoff_zone_id: Dropoff zone ID
    - passenger_count: Number of passengers
    - limit: Maximum number of results (default 100)
    - offset: Pagination offset (default 0)
    - sort_by: Field to sort by
    - sort_order: 'asc' or 'desc'
    """
    try:
        session = get_session()
        
        query = session.query(Trip).join(Trip.pickup_zone).join(
            Trip.dropoff_zone,
            Trip.dropoff_zone_id == Zone.zone_id
        )

        filters = build_trip_filters(request.args)

        if filters:
            query = query.filter(and_(*filters))
        
        # Get total count
        total_count = query.count()
        
        # Sorting
        sort_by = request.args.get('sort_by', 'pickup_datetime')
        sort_order = request.args.get('sort_order', 'desc')
        
        if hasattr(Trip, sort_by):
            order_column = getattr(Trip, sort_by)
            if sort_order == 'desc':
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(order_column)
        
        # Pagination
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        
        trips = query.limit(limit).offset(offset).all()
        
        # Convert to dict
        trips_data = [trip.to_dict() for trip in trips]
        
        session.close()
        
        return jsonify({
            'trips': trips_data,
            'total_count': total_count,
            'limit': limit,
            'offset': offset
        })
    
    except Exception as e:
        logger.error(f"Error fetching trips: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get aggregate statistics.
    
    Query Parameters:
    - start_date: Start date for statistics
    - end_date: End date for statistics
    - group_by: Group by 'hour', 'day', 'zone', or 'payment_type'
    """
    try:
        session = get_session()

        filters = build_trip_filters(request.args)

        overall_query = session.query(
            func.count(Trip.trip_id).label('total_trips'),
            func.avg(Trip.fare_amount).label('avg_fare'),
            func.avg(Trip.trip_distance).label('avg_distance'),
            func.avg(Trip.trip_duration).label('avg_duration'),
            func.avg(Trip.trip_speed).label('avg_speed'),
            func.sum(Trip.total_amount).label('total_revenue')
        )

        if filters:
            overall_query = overall_query.filter(and_(*filters))

        overall_stats = overall_query.first()
        
        stats = {
            'total_trips': overall_stats.total_trips or 0,
            'avg_fare': round(float(overall_stats.avg_fare or 0), 2),
            'avg_distance': round(float(overall_stats.avg_distance or 0), 2),
            'avg_duration': round(float(overall_stats.avg_duration or 0), 2),
            'avg_speed': round(float(overall_stats.avg_speed or 0), 2),
            'total_revenue': round(float(overall_stats.total_revenue or 0), 2)
        }
        
        # Group by statistics
        group_by = request.args.get('group_by')
        grouped_stats = []
        
        if group_by == 'hour':
            group_query = session.query(
                extract('hour', Trip.pickup_datetime).label('hour'),
                func.count(Trip.trip_id).label('trip_count'),
                func.avg(Trip.fare_amount).label('avg_fare'),
                func.avg(Trip.trip_speed).label('avg_speed')
            )

            if filters:
                group_query = group_query.filter(and_(*filters))

            results = group_query.group_by('hour').order_by('hour').all()
            
            grouped_stats = [{
                'hour': int(r.hour),
                'trip_count': r.trip_count,
                'avg_fare': round(float(r.avg_fare or 0), 2),
                'avg_speed': round(float(r.avg_speed or 0), 2)
            } for r in results]
        
        elif group_by == 'zone':
            group_query = session.query(
                Zone.zone_name,
                Zone.borough,
                func.count(Trip.trip_id).label('trip_count'),
                func.avg(Trip.fare_amount).label('avg_fare')
            ).join(Trip.pickup_zone)

            if filters:
                group_query = group_query.filter(and_(*filters))

            results = group_query.group_by(Zone.zone_name, Zone.borough).order_by(
                desc('trip_count')
            ).limit(20).all()
            
            grouped_stats = [{
                'zone_name': r.zone_name,
                'borough': r.borough,
                'trip_count': r.trip_count,
                'avg_fare': round(float(r.avg_fare or 0), 2)
            } for r in results]
        
        elif group_by == 'payment_type':
            group_query = session.query(
                PaymentType.payment_name,
                func.count(Trip.trip_id).label('trip_count'),
                func.avg(Trip.fare_amount).label('avg_fare')
            ).join(Trip.payment_type)

            if filters:
                group_query = group_query.filter(and_(*filters))

            results = group_query.group_by(PaymentType.payment_name).all()
            
            grouped_stats = [{
                'payment_type': r.payment_name,
                'trip_count': r.trip_count,
                'avg_fare': round(float(r.avg_fare or 0), 2)
            } for r in results]
        
        session.close()
        
        return jsonify({
            'overall': stats,
            'grouped': grouped_stats
        })
    
    except Exception as e:
        logger.error(f"Error calculating statistics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/zones', methods=['GET'])
def get_zones():
    """Get list of all taxi zones."""
    try:
        session = get_session()
        zones = session.query(Zone).order_by(Zone.borough, Zone.zone_name).all()
        
        zones_data = [{
            'zone_id': z.zone_id,
            'zone_name': z.zone_name,
            'borough': z.borough,
            'service_zone': z.service_zone
        } for z in zones]
        
        session.close()
        
        return jsonify({'zones': zones_data})
    
    except Exception as e:
        logger.error(f"Error fetching zones: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/time-series', methods=['GET'])
def get_time_series():
    """
    Get time series data for visualizations.
    
    Query Parameters:
    - start_date: Start date
    - end_date: End date
    - interval: 'hour', 'day', or 'week'
    - metric: 'trip_count', 'avg_fare', 'avg_speed', 'total_revenue'
    """
    try:
        session = get_session()
        
        # Parse parameters
        interval = request.args.get('interval', 'hour')
        metric = request.args.get('metric', 'trip_count')
        
        filters = build_trip_filters(request.args)

        # Build query based on interval
        if interval == 'hour':
            query = session.query(
                extract('hour', Trip.pickup_datetime).label('time_unit'),
                func.count(Trip.trip_id).label('trip_count'),
                func.avg(Trip.fare_amount).label('avg_fare'),
                func.avg(Trip.trip_speed).label('avg_speed'),
                func.sum(Trip.total_amount).label('total_revenue')
            )

            if filters:
                query = query.filter(and_(*filters))

            results = query.group_by('time_unit').order_by('time_unit').all()
            
            time_series = [{
                'hour': int(r.time_unit),
                'trip_count': r.trip_count,
                'avg_fare': round(float(r.avg_fare or 0), 2),
                'avg_speed': round(float(r.avg_speed or 0), 2),
                'total_revenue': round(float(r.total_revenue or 0), 2)
            } for r in results]
        
        elif interval == 'day':
            query = session.query(
                func.date(Trip.pickup_datetime).label('date'),
                func.count(Trip.trip_id).label('trip_count'),
                func.avg(Trip.fare_amount).label('avg_fare'),
                func.avg(Trip.trip_speed).label('avg_speed'),
                func.sum(Trip.total_amount).label('total_revenue')
            )

            if filters:
                query = query.filter(and_(*filters))

            results = query.group_by('date').order_by('date').all()

            time_series = [{
                'date': str(r.date),
                'trip_count': r.trip_count,
                'avg_fare': round(float(r.avg_fare or 0), 2),
                'avg_speed': round(float(r.avg_speed or 0), 2),
                'total_revenue': round(float(r.total_revenue or 0), 2)
            } for r in results]
        
        session.close()
        
        return jsonify({'time_series': time_series})
    
    except Exception as e:
        logger.error(f"Error generating time series: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/heatmap', methods=['GET'])
def get_heatmap():
    """Get heatmap data for pickup/dropoff locations."""
    try:
        session = get_session()
        
        filters = build_trip_filters(request.args)
        
        # Pickup heatmap
        pickup_query = session.query(
            Zone.zone_id,
            Zone.zone_name,
            Zone.borough,
            func.count(Trip.trip_id).label('pickup_count')
        ).join(Trip.pickup_zone)

        if filters:
            pickup_query = pickup_query.filter(and_(*filters))

        pickup_data = pickup_query.group_by(Zone.zone_id, Zone.zone_name, Zone.borough).order_by(
            desc('pickup_count')
        ).limit(50).all()
        
        # Dropoff heatmap
        dropoff_query = session.query(
            Zone.zone_id,
            Zone.zone_name,
            Zone.borough,
            func.count(Trip.trip_id).label('dropoff_count')
        ).join(Trip.dropoff_zone)

        if filters:
            dropoff_query = dropoff_query.filter(and_(*filters))

        dropoff_data = dropoff_query.group_by(Zone.zone_id, Zone.zone_name, Zone.borough).order_by(
            desc('dropoff_count')
        ).limit(50).all()
        
        session.close()
        
        return jsonify({
            'pickup': [{
                'zone_id': r.zone_id,
                'zone_name': r.zone_name,
                'borough': r.borough,
                'count': r.pickup_count
            } for r in pickup_data],
            'dropoff': [{
                'zone_id': r.zone_id,
                'zone_name': r.zone_name,
                'borough': r.borough,
                'count': r.dropoff_count
            } for r in dropoff_data]
        })
    
    except Exception as e:
        logger.error(f"Error generating heatmap: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/anomalies', methods=['GET'])
def get_anomalies():
    """
    Detect anomalies using custom algorithm.
    
    Query Parameters:
    - field: Field to check ('fare_amount', 'trip_duration', 'trip_speed')
    - threshold: Z-score threshold (default 3.0)
    - limit: Number of results (default 100)
    """
    try:
        session = get_session()
        
        field = request.args.get('field', 'fare_amount')
        threshold = float(request.args.get('threshold', 3.0))
        limit = int(request.args.get('limit', 100))
        
        # Fetch sample of trips
        trips = session.query(Trip).limit(10000).all()
        trips_data = [trip.to_dict() for trip in trips]
        
        # Use custom anomaly detection algorithm
        anomalies = AnomalyDetector.detect_outliers(trips_data, field, threshold)
        
        session.close()
        
        return jsonify({
            'anomalies': anomalies[:limit],
            'total_anomalies': len(anomalies),
            'field': field,
            'threshold': threshold
        })
    
    except Exception as e:
        logger.error(f"Error detecting anomalies: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/top-routes', methods=['GET'])
def get_top_routes():
    """Get top routes by trip count."""
    try:
        session = get_session()
        
        limit = int(request.args.get('limit', 20))
        
        results = session.query(
            Zone.zone_name.label('pickup_zone'),
            Zone.zone_id.label('pickup_zone_id'),
            func.count(Trip.trip_id).label('trip_count'),
            func.avg(Trip.fare_amount).label('avg_fare'),
            func.avg(Trip.trip_distance).label('avg_distance')
        ).join(Trip.pickup_zone).group_by(
            Zone.zone_name, Zone.zone_id
        ).order_by(desc('trip_count')).limit(limit).all()
        
        routes = [{
            'pickup_zone': r.pickup_zone,
            'pickup_zone_id': r.pickup_zone_id,
            'trip_count': r.trip_count,
            'avg_fare': round(float(r.avg_fare or 0), 2),
            'avg_distance': round(float(r.avg_distance or 0), 2)
        } for r in results]
        
        session.close()
        
        return jsonify({'routes': routes})
    
    except Exception as e:
        logger.error(f"Error fetching top routes: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        session = get_session()
        trip_count = session.query(func.count(Trip.trip_id)).scalar()
        session.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'trip_count': trip_count
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
