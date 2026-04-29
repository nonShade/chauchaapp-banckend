"""
In-memory token blacklist for JWT logout support.

Uses a singleton pattern to maintain a global blacklist of JTI (JWT ID)
values. Expired entries are automatically cleaned up.

Note:
    For production, replace with a Redis-based implementation
    to support horizontal scaling.
"""

import threading
from datetime import datetime, timezone


class TokenBlacklist:
    """Thread-safe in-memory token blacklist with TTL-based cleanup."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._blacklist: dict[str, datetime] = {}
            return cls._instance

    def blacklist_token(self, jti: str, exp: datetime) -> None:
        """Add a token JTI to the blacklist.

        Args:
            jti: The JWT ID to blacklist.
            exp: The token's expiration datetime (entry auto-removed after this).
        """
        self._blacklist[jti] = exp
        self._cleanup()

    def is_blacklisted(self, jti: str) -> bool:
        """Check if a token JTI is blacklisted.

        Args:
            jti: The JWT ID to check.

        Returns:
            True if the token is blacklisted, False otherwise.
        """
        self._cleanup()
        return jti in self._blacklist

    def _cleanup(self) -> None:
        """Remove expired entries from the blacklist."""
        now = datetime.now(timezone.utc)
        expired = [jti for jti, exp in self._blacklist.items() if exp < now]
        for jti in expired:
            del self._blacklist[jti]

    def clear(self) -> None:
        """Clear all entries (useful for testing)."""
        self._blacklist.clear()


token_blacklist = TokenBlacklist()
