# app/monitoring/attack_detection.py
import time
from typing import Dict, List, Any
from collections import defaultdict
import json

class AttackDetector:
    """Detects potential attacks based on security events"""
    
    def __init__(self):
        # Track recent events by user
        self.recent_events = defaultdict(list)
        # Maximum number of events to store per user
        self.max_events = 100
        # Timeframe for rate limiting (seconds)
        self.rate_limit_window = 60
        # Maximum events in rate limit window
        self.rate_limit_max = 30
        
    def track_event(self, user_id: str, event_type: str, metadata: Dict = None):
        """Track a user event for attack detection"""
        now = time.time()
        
        # Add event to user's history
        self.recent_events[user_id].append({
            "timestamp": now,
            "event_type": event_type,
            "metadata": metadata or {}
        })
        
        # Trim history if needed
        if len(self.recent_events[user_id]) > self.max_events:
            self.recent_events[user_id] = self.recent_events[user_id][-self.max_events:]
            
        # Check for potential attacks
        return self.check_for_attacks(user_id)
        
    def check_for_attacks(self, user_id: str) -> Dict:
        """Check for potential attacks based on user history"""
        user_events = self.recent_events[user_id]
        now = time.time()
        
        # No events, no attacks
        if not user_events:
            return {"attacks_detected": []}
            
        attacks = []
        
        # Check for rate limiting
        recent_events = [e for e in user_events if now - e["timestamp"] <= self.rate_limit_window]
        if len(recent_events) > self.rate_limit_max:
            attacks.append({
                "type": "rate_limit_breach",
                "severity": "medium",
                "details": f"{len(recent_events)} events in {self.rate_limit_window} seconds"
            })
            
        # Check for repeated validation failures
        validation_failures = [e for e in recent_events 
                              if e["event_type"] == "input_validation" and 
                              e.get("metadata", {}).get("risk_level") == "High"]
        if len(validation_failures) >= 3:
            attacks.append({
                "type": "repeated_validation_failures",
                "severity": "high",
                "details": f"{len(validation_failures)} high-risk validation failures"
            })
            
        # Check for vector DB manipulation attempts
        vector_queries = [e for e in recent_events if e["event_type"] == "vector_db_query"]
        if len(vector_queries) >= 10:
            # Check for similarity flooding (many queries with low match results)
            low_result_queries = [q for q in vector_queries 
                                if q.get("metadata", {}).get("results_count", 0) <= 1]
            if len(low_result_queries) >= 5:
                attacks.append({
                    "type": "vector_db_probing",
                    "severity": "medium",
                    "details": "Multiple queries with few results"
                })
                
        return {"attacks_detected": attacks}