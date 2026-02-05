"""Database models and setup for experiment tracking"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager for experiment tracking"""
    
    def __init__(self, db_path: str = "mlops.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Experiments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id TEXT UNIQUE,
                experiment_name TEXT NOT NULL,
                function_name TEXT,
                module TEXT,
                status TEXT DEFAULT 'running',
                start_time TEXT,
                end_time TEXT,
                duration REAL,
                result TEXT,
                error TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Parameters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id TEXT,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
            )
        """)
        
        # Metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id TEXT,
                key TEXT NOT NULL,
                value REAL NOT NULL,
                step INTEGER,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")
    
    def save_experiment(self, data: Dict[str, Any]) -> str:
        """Save or update experiment data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        experiment_id = data.get("experiment_id")
        if not experiment_id:
            # Generate new experiment ID
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            experiment_id = f"exp_{timestamp}"
        
        # Check if experiment exists
        cursor.execute("SELECT id FROM experiments WHERE experiment_id = ?", (experiment_id,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing experiment
            cursor.execute("""
                UPDATE experiments 
                SET status = ?, end_time = ?, duration = ?, result = ?, error = ?
                WHERE experiment_id = ?
            """, (
                data.get("status", "running"),
                data.get("end_time"),
                data.get("duration"),
                data.get("result"),
                data.get("error"),
                experiment_id
            ))
        else:
            # Insert new experiment
            cursor.execute("""
                INSERT INTO experiments 
                (experiment_id, experiment_name, function_name, module, status, start_time)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                experiment_id,
                data.get("experiment_name"),
                data.get("function_name"),
                data.get("module"),
                data.get("status", "running"),
                data.get("start_time")
            ))
            
            # Save parameters
            parameters = data.get("parameters", {})
            for key, value in parameters.items():
                cursor.execute("""
                    INSERT INTO parameters (experiment_id, key, value)
                    VALUES (?, ?, ?)
                """, (experiment_id, key, json.dumps(value)))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved experiment: {experiment_id}")
        return experiment_id
    
    def get_experiment(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve experiment by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM experiments WHERE experiment_id = ?", (experiment_id,))
        exp_row = cursor.fetchone()
        
        if not exp_row:
            conn.close()
            return None
        
        experiment = dict(exp_row)
        
        # Get parameters
        cursor.execute("SELECT key, value FROM parameters WHERE experiment_id = ?", (experiment_id,))
        params = {row["key"]: json.loads(row["value"]) for row in cursor.fetchall()}
        experiment["parameters"] = params
        
        # Get metrics
        cursor.execute("SELECT key, value, step, timestamp FROM metrics WHERE experiment_id = ?", (experiment_id,))
        metrics = [dict(row) for row in cursor.fetchall()]
        experiment["metrics"] = metrics
        
        conn.close()
        return experiment
    
    def get_all_experiments(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all experiments"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT experiment_id, experiment_name, status, start_time, duration, created_at
            FROM experiments 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        experiments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return experiments
    
    def log_metric(self, experiment_id: str, key: str, value: float, step: Optional[int] = None):
        """Log a metric for an experiment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO metrics (experiment_id, key, value, step)
            VALUES (?, ?, ?, ?)
        """, (experiment_id, key, value, step))
        
        conn.commit()
        conn.close()
        logger.info(f"Logged metric {key}={value} for experiment {experiment_id}")
