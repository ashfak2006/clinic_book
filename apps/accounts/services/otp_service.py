import logging
import secrets
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache

logger = logging.getLogger(__name__)


class OTPService:
    OTP_TTL = 300  # 5 minutes
    MAX_ATTEMPTS = 5

    @staticmethod
    def generate_otp() -> str:
        return str(secrets.randbelow(900000) + 100000)

    @classmethod
    def request_otp(cls, key: str) -> str:
        otp = cls.generate_otp()
        otp_key = f"otp:code:{key}"
        attempts_key = f"otp:attempts:{key}"

        logger.info("OTP requested for key: %s", key)

        cache.set(otp_key, make_password(otp), timeout=cls.OTP_TTL)
        cache.set(attempts_key, 0, timeout=cls.OTP_TTL)

        return otp

    @classmethod
    def verify_otp(cls, key: str, entered_otp: str):
        otp_key = f"otp:code:{key}"
        attempts_key = f"otp:attempts:{key}"
        otp_hash = cache.get(otp_key)

        if not otp_hash:
            return False, "OTP expired or not found"

        attempts = cache.get(attempts_key, 0)
        if attempts >= cls.MAX_ATTEMPTS:
            cache.delete_many([otp_key, attempts_key])
            return False, "Too many attempts. Please request a new OTP."

        if not check_password(entered_otp, otp_hash):
            try:
                cache.incr(attempts_key)
            except ValueError:
                cache.set(attempts_key, 1, timeout=cls.OTP_TTL)
            return False, "Invalid OTP"

        cache.delete_many([otp_key, attempts_key])
        return True, "OTP verified"
