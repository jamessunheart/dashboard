"""
Database setup and models for Full Potential Membership
Simple SQLite database for user management
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import hashlib
import secrets

# Database path
DB_PATH = Path(__file__).parent.parent / "membership.db"


def get_db():
    """Get database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with required tables"""
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            membership_tier TEXT NOT NULL DEFAULT 'seeker',
            created_at TEXT NOT NULL,
            last_login TEXT,
            is_active INTEGER DEFAULT 1,
            stripe_customer_id TEXT
        )
    ''')

    # Sessions table (for auth tokens)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # User progress table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal_data TEXT,
            reflection_data TEXT,
            strengths_data TEXT,
            last_updated TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${pwd_hash}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    try:
        salt, pwd_hash = password_hash.split('$')
        return pwd_hash == hashlib.sha256((password + salt).encode()).hexdigest()
    except Exception:
        return False


def create_user(email: str, password: str, full_name: str, tier: str = 'seeker') -> Optional[int]:
    """Create new user, returns user_id or None if email exists"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        password_hash = hash_password(password)
        created_at = datetime.utcnow().isoformat()

        cursor.execute('''
            INSERT INTO users (email, password_hash, full_name, membership_tier, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, password_hash, full_name, tier, created_at))

        user_id = cursor.lastrowid

        # Initialize progress tracking
        cursor.execute('''
            INSERT INTO user_progress (user_id, last_updated)
            VALUES (?, ?)
        ''', (user_id, created_at))

        conn.commit()
        conn.close()

        return user_id
    except sqlite3.IntegrityError:
        return None


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def create_session(user_id: int, duration_hours: int = 24) -> str:
    """Create new session token for user"""
    from datetime import timedelta

    conn = get_db()
    cursor = conn.cursor()

    token = secrets.token_urlsafe(32)
    created_at = datetime.utcnow()
    expires_at = created_at + timedelta(hours=duration_hours)

    cursor.execute('''
        INSERT INTO sessions (user_id, token, created_at, expires_at)
        VALUES (?, ?, ?, ?)
    ''', (user_id, token, created_at.isoformat(), expires_at.isoformat()))

    # Update last login
    cursor.execute('''
        UPDATE users SET last_login = ? WHERE id = ?
    ''', (created_at.isoformat(), user_id))

    conn.commit()
    conn.close()

    return token


def verify_session(token: str) -> Optional[Dict[str, Any]]:
    """Verify session token and return user if valid"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT users.* FROM users
        JOIN sessions ON users.id = sessions.user_id
        WHERE sessions.token = ? AND sessions.expires_at > ? AND users.is_active = 1
    ''', (token, datetime.utcnow().isoformat()))

    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def delete_session(token: str):
    """Delete session (logout)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sessions WHERE token = ?', (token,))
    conn.commit()
    conn.close()


# Initialize database on import
init_db()
