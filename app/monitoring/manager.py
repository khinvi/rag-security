# app/monitoring/manager.py
from .logger import SecurityLogger
from .attack_detection import AttackDetector

class SecurityMonitoringManager:
    """Manages security monitoring for the RAG system"""
    
    def __init__(self):
        self.logger = SecurityLogger()
        self.detector = AttackDetector()
        
    async def track_security_event(self, event_type: str, user_id: str, **kwargs):
        """Track a security event and check for potential attacks"""
        # Log the event
        log_entry = self.logger.log_security_event(
            event_type=event_type,
            user_id=user_id,
            **kwargs
        )
        
        # Track in attack detector
        attack_results = self.detector.track_event(
            user_id=user_id,
            event_type=event_type,
            metadata=kwargs
        )
        
        # If attacks detected, log them
        if attack_results["attacks_detected"]:
            for attack in attack_results["attacks_detected"]:
                self.logger.log_security_event(
                    event_type="attack_detected",
                    user_id=user_id,
                    attack_type=attack["type"],
                    severity=attack["severity"],
                    details=attack["details"]
                )
                
        return {
            "event_logged": log_entry,
            "attacks_detected": attack_results["attacks_detected"]
        }