#!/usr/bin/env python3
"""
Comprehensive monitoring and alerting system
Tracks system health, performance, and sends notifications
"""

import os
import time
import json
import smtplib
import psutil
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from database.service import DatabaseService

class SystemMonitor:
    def __init__(self):
        self.alerts_sent = {}
        self.metrics_history = []
        self.alert_cooldown = 300  # 5 minutes
        
    def collect_system_metrics(self) -> Dict:
        """Collect system performance metrics"""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "network_io": psutil.net_io_counters()._asdict(),
            "process_count": len(psutil.pids())
        }
    
    def collect_application_metrics(self) -> Dict:
        """Collect application-specific metrics"""
        try:
            with DatabaseService() as db:
                orders = db.get_orders()
                returns = db.get_returns()
                
                # Calculate business metrics
                total_orders = len(orders)
                pending_orders = len([o for o in orders if o.get('Status') == 'Processing'])
                total_returns = len(returns)
                
                # Get recent activity (last 24 hours)
                recent_cutoff = datetime.now() - timedelta(hours=24)
                recent_orders = len([o for o in orders if 'OrderDate' in o and 
                                   datetime.fromisoformat(o['OrderDate']) > recent_cutoff])
                
                return {
                    "total_orders": total_orders,
                    "pending_orders": pending_orders,
                    "total_returns": total_returns,
                    "recent_orders_24h": recent_orders,
                    "order_processing_rate": recent_orders / 24 if recent_orders > 0 else 0
                }
        except Exception as e:
            return {"error": str(e)}
    
    def check_api_health(self) -> Dict:
        """Check API endpoint health"""
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds(),
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def check_agent_health(self) -> Dict:
        """Check agent system health"""
        try:
            # Check if agent log file exists and is recent
            log_file = "data/logs.csv"
            if os.path.exists(log_file):
                stat = os.stat(log_file)
                last_modified = datetime.fromtimestamp(stat.st_mtime)
                age_hours = (datetime.now() - last_modified).total_seconds() / 3600
                
                return {
                    "status": "healthy" if age_hours < 1 else "stale",
                    "last_activity": last_modified.isoformat(),
                    "age_hours": age_hours
                }
            else:
                return {"status": "no_activity", "error": "No log file found"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def detect_anomalies(self, metrics: Dict) -> List[Dict]:
        """Detect system anomalies and issues"""
        anomalies = []
        
        # High resource usage
        if metrics.get("cpu_percent", 0) > 80:
            anomalies.append({
                "type": "high_cpu",
                "severity": "warning",
                "message": f"High CPU usage: {metrics['cpu_percent']:.1f}%"
            })
        
        if metrics.get("memory_percent", 0) > 85:
            anomalies.append({
                "type": "high_memory",
                "severity": "critical",
                "message": f"High memory usage: {metrics['memory_percent']:.1f}%"
            })
        
        if metrics.get("disk_percent", 0) > 90:
            anomalies.append({
                "type": "high_disk",
                "severity": "critical",
                "message": f"High disk usage: {metrics['disk_percent']:.1f}%"
            })
        
        # Application-specific anomalies
        app_metrics = metrics.get("application", {})
        if app_metrics.get("pending_orders", 0) > 100:
            anomalies.append({
                "type": "high_pending_orders",
                "severity": "warning",
                "message": f"High pending orders: {app_metrics['pending_orders']}"
            })
        
        # API health issues
        api_health = metrics.get("api", {})
        if api_health.get("status") != "healthy":
            anomalies.append({
                "type": "api_unhealthy",
                "severity": "critical",
                "message": f"API unhealthy: {api_health.get('error', 'Unknown error')}"
            })
        
        return anomalies
    
    def send_email_alert(self, subject: str, body: str) -> bool:
        """Send email alert"""
        try:
            smtp_host = os.getenv("SMTP_HOST")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_user = os.getenv("SMTP_USER")
            smtp_password = os.getenv("SMTP_PASSWORD")
            alert_recipients = os.getenv("ALERT_RECIPIENTS", "").split(",")
            
            if not all([smtp_host, smtp_user, smtp_password]) or not alert_recipients:
                print("⚠️  Email configuration incomplete, skipping email alert")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = ", ".join(alert_recipients)
            msg['Subject'] = f"[AI Agent Alert] {subject}"
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            server.quit()
            
            print(f"📧 Email alert sent: {subject}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email alert: {e}")
            return False
    
    def send_slack_alert(self, message: str) -> bool:
        """Send Slack alert"""
        try:
            webhook_url = os.getenv("SLACK_WEBHOOK_URL")
            if not webhook_url:
                return False
            
            import requests
            payload = {
                "text": f"🚨 AI Agent Alert: {message}",
                "username": "AI Agent Monitor"
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"💬 Slack alert sent: {message}")
                return True
            else:
                print(f"❌ Slack alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to send Slack alert: {e}")
            return False
    
    def should_send_alert(self, alert_type: str) -> bool:
        """Check if we should send an alert (respects cooldown)"""
        now = time.time()
        last_sent = self.alerts_sent.get(alert_type, 0)
        
        if now - last_sent > self.alert_cooldown:
            self.alerts_sent[alert_type] = now
            return True
        return False
    
    def handle_anomalies(self, anomalies: List[Dict]):
        """Handle detected anomalies"""
        for anomaly in anomalies:
            alert_type = anomaly["type"]
            severity = anomaly["severity"]
            message = anomaly["message"]
            
            if self.should_send_alert(alert_type):
                print(f"🚨 {severity.upper()}: {message}")
                
                # Send alerts based on severity
                if severity == "critical":
                    self.send_email_alert(f"Critical Alert: {alert_type}", message)
                    self.send_slack_alert(message)
                elif severity == "warning":
                    self.send_slack_alert(message)
    
    def generate_health_report(self, metrics: Dict) -> str:
        """Generate comprehensive health report"""
        report = []
        report.append("🏥 AI Agent System Health Report")
        report.append("=" * 40)
        report.append(f"Timestamp: {metrics['timestamp']}")
        report.append("")
        
        # System metrics
        report.append("💻 System Metrics:")
        report.append(f"  CPU Usage: {metrics.get('cpu_percent', 0):.1f}%")
        report.append(f"  Memory Usage: {metrics.get('memory_percent', 0):.1f}%")
        report.append(f"  Disk Usage: {metrics.get('disk_percent', 0):.1f}%")
        report.append("")
        
        # Application metrics
        app_metrics = metrics.get("application", {})
        if app_metrics and "error" not in app_metrics:
            report.append("📊 Application Metrics:")
            report.append(f"  Total Orders: {app_metrics.get('total_orders', 0)}")
            report.append(f"  Pending Orders: {app_metrics.get('pending_orders', 0)}")
            report.append(f"  Total Returns: {app_metrics.get('total_returns', 0)}")
            report.append(f"  Recent Orders (24h): {app_metrics.get('recent_orders_24h', 0)}")
            report.append("")
        
        # API health
        api_health = metrics.get("api", {})
        report.append("🔗 API Health:")
        report.append(f"  Status: {api_health.get('status', 'unknown')}")
        if "response_time" in api_health:
            report.append(f"  Response Time: {api_health['response_time']:.3f}s")
        report.append("")
        
        # Agent health
        agent_health = metrics.get("agent", {})
        report.append("🤖 Agent Health:")
        report.append(f"  Status: {agent_health.get('status', 'unknown')}")
        if "last_activity" in agent_health:
            report.append(f"  Last Activity: {agent_health['last_activity']}")
        
        return "\n".join(report)
    
    def run_monitoring_cycle(self):
        """Run one monitoring cycle"""
        print("🔍 Running monitoring cycle...")
        
        # Collect all metrics
        metrics = {
            "timestamp": datetime.now().isoformat(),
            **self.collect_system_metrics(),
            "application": self.collect_application_metrics(),
            "api": self.check_api_health(),
            "agent": self.check_agent_health()
        }
        
        # Store metrics history
        self.metrics_history.append(metrics)
        
        # Keep only last 100 entries
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        # Detect and handle anomalies
        anomalies = self.detect_anomalies(metrics)
        if anomalies:
            self.handle_anomalies(anomalies)
        
        # Save metrics to file
        with open("data/monitoring_metrics.json", "w") as f:
            json.dump(self.metrics_history, f, indent=2)
        
        # Generate and save health report
        report = self.generate_health_report(metrics)
        with open("data/health_report.txt", "w") as f:
            f.write(report)
        
        print(f"✅ Monitoring cycle completed - {len(anomalies)} anomalies detected")
        return metrics, anomalies

def main():
    """Main monitoring loop"""
    monitor = SystemMonitor()
    
    print("🔍 Starting AI Agent System Monitor")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            monitor.run_monitoring_cycle()
            
            # Wait for next cycle
            interval = int(os.getenv("MONITORING_INTERVAL", "60"))  # 1 minute default
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")

if __name__ == "__main__":
    main()