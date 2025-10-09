#!/usr/bin/env python3
"""
Authentication and Authorization System for AI Agent Logistics
Implements JWT-based authentication with role-based access control
"""

import jwt
import bcrypt
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ai-agent-logistics-secret-key-2025")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Security scheme
security = HTTPBearer()

# User models
class User(BaseModel):
    user_id: str
    username: str
    email: str
    role: str
    permissions: List[str]
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "operator"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

# Role-based permissions
ROLE_PERMISSIONS = {
    "admin": [
        "read:all", "write:all", "delete:all",
        "manage:users", "manage:system", "manage:agents",
        "view:dashboard", "view:analytics", "manage:alerts"
    ],
    "manager": [
        "read:orders", "read:inventory", "read:shipments",
        "write:orders", "write:inventory", "approve:reviews",
        "view:dashboard", "view:analytics", "manage:alerts",
        "run:agents"
    ],
    "operator": [
        "read:orders", "read:inventory", "read:shipments",
        "write:orders", "update:shipments",
        "view:dashboard", "create:reviews"
    ],
    "viewer": [
        "read:orders", "read:inventory", "read:shipments",
        "view:dashboard"
    ]
}

class AuthSystem:
    """Authentication and authorization system"""
    
    def __init__(self):
        # In-memory user store (in production, use database)
        self.users = {}
        self.refresh_tokens = {}
        self._create_default_users()
    
    def _create_default_users(self):
        """Create default users for demo"""
        default_users = [
            {
                "username": "admin",
                "email": "admin@logistics.ai",
                "password": "admin123",
                "role": "admin"
            },
            {
                "username": "manager",
                "email": "manager@logistics.ai", 
                "password": "manager123",
                "role": "manager"
            },
            {
                "username": "operator",
                "email": "operator@logistics.ai",
                "password": "operator123", 
                "role": "operator"
            },
            {
                "username": "viewer",
                "email": "viewer@logistics.ai",
                "password": "viewer123",
                "role": "viewer"
            }
        ]
        
        for user_data in default_users:
            self.create_user(UserCreate(**user_data))
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        if user_data.username in self.users:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )
        
        user_id = str(uuid.uuid4())
        hashed_password = self._hash_password(user_data.password)
        
        user = User(
            user_id=user_id,
            username=user_data.username,
            email=user_data.email,
            role=user_data.role,
            permissions=ROLE_PERMISSIONS.get(user_data.role, []),
            created_at=datetime.utcnow()
        )
        
        self.users[user_data.username] = {
            "user": user,
            "password_hash": hashed_password
        }
        
        return user
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user credentials"""
        user_data = self.users.get(username)
        if not user_data:
            return None
        
        if not self._verify_password(password, user_data["password_hash"]):
            return None
        
        # Update last login
        user_data["user"].last_login = datetime.utcnow()
        return user_data["user"]
    
    def create_access_token(self, user: User) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": user.username,
            "user_id": user.user_id,
            "role": user.role,
            "permissions": user.permissions,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    def create_refresh_token(self, user: User) -> str:
        """Create JWT refresh token"""
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        token_id = str(uuid.uuid4())
        
        payload = {
            "sub": user.username,
            "user_id": user.user_id,
            "token_id": token_id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        
        refresh_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        self.refresh_tokens[token_id] = {
            "user_id": user.user_id,
            "created_at": datetime.utcnow(),
            "expires_at": expire
        }
        
        return refresh_token
    
    def verify_token(self, token: str) -> Dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
        """Get current authenticated user"""
        token = credentials.credentials
        payload = self.verify_token(token)
        
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        username = payload.get("sub")
        user_data = self.users.get(username)
        
        if not user_data or not user_data["user"].is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        return user_data["user"]
    
    def require_permission(self, required_permission: str):
        """Decorator to require specific permission"""
        def permission_checker(current_user: User = Depends(self.get_current_user)):
            if required_permission not in current_user.permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission required: {required_permission}"
                )
            return current_user
        return permission_checker
    
    def require_role(self, required_role: str):
        """Decorator to require specific role"""
        def role_checker(current_user: User = Depends(self.get_current_user)):
            if current_user.role != required_role and current_user.role != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role required: {required_role}"
                )
            return current_user
        return role_checker
    
    def login(self, login_data: UserLogin) -> Token:
        """User login"""
        user = self.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        access_token = self.create_access_token(user)
        refresh_token = self.create_refresh_token(user)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    def refresh_access_token(self, refresh_token: str) -> Token:
        """Refresh access token"""
        payload = self.verify_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        token_id = payload.get("token_id")
        if token_id not in self.refresh_tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token revoked"
            )
        
        username = payload.get("sub")
        user_data = self.users.get(username)
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        user = user_data["user"]
        new_access_token = self.create_access_token(user)
        
        return Token(
            access_token=new_access_token,
            refresh_token=refresh_token,  # Keep same refresh token
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    def logout(self, refresh_token: str) -> bool:
        """User logout - revoke refresh token"""
        try:
            payload = self.verify_token(refresh_token)
            token_id = payload.get("token_id")
            
            if token_id in self.refresh_tokens:
                del self.refresh_tokens[token_id]
                return True
        except:
            pass
        
        return False
    
    def get_user_info(self, username: str) -> Optional[User]:
        """Get user information"""
        user_data = self.users.get(username)
        return user_data["user"] if user_data else None
    
    def list_users(self) -> List[User]:
        """List all users (admin only)"""
        return [data["user"] for data in self.users.values()]

# Global auth system instance
auth_system = AuthSystem()

# Dependency functions for FastAPI
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    return auth_system.get_current_user(credentials)

def require_permission(permission: str):
    return auth_system.require_permission(permission)

def require_role(role: str):
    return auth_system.require_role(role)

# Test authentication system
if __name__ == "__main__":
    print("🔒 Testing Authentication System")
    print("=" * 50)
    
    # Test user creation
    print("👤 Default users created:")
    for username, data in auth_system.users.items():
        user = data["user"]
        print(f"   • {username} ({user.role}) - {len(user.permissions)} permissions")
    
    # Test login
    print("\n🔑 Testing login:")
    try:
        token = auth_system.login(UserLogin(username="admin", password="admin123"))
        print(f"✅ Admin login successful")
        print(f"   Access token: {token.access_token[:50]}...")
        
        # Test token verification
        payload = auth_system.verify_token(token.access_token)
        print(f"✅ Token verification successful")
        print(f"   User: {payload['sub']}, Role: {payload['role']}")
        
    except Exception as e:
        print(f"❌ Login test failed: {e}")
    
    print("\n🚀 Authentication system ready!")
