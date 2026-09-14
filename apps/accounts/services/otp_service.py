import secrets

from django.core.cache import cache
from django.contrib.auth.hashers import (
    make_password,
    check_password
)




class OTPService:
    OTP_TTL = 300  # 5 minutes
    MAX_ATTEMPTS = 5
    @staticmethod
    def generate_otp():
        return str(
            secrets.randbelow(900000) + 100000
        )

    @staticmethod
    def request_otp(key):
        OTP_TTL=300
        otp = OTPService.generate_otp()

        otp_key = f"otp:code:{key}"
        attempts_key = f"otp:attempts:{key}"
        print(f"Generated OTP for {otp_key}: {otp}")
        
        cache.set(
            otp_key,
            make_password(otp),
            timeout=OTP_TTL
        )

        cache.set(
            attempts_key,
            0,
            timeout=OTP_TTL
        )

        return otp

    @staticmethod
    def verify_otp(key, entered_otp):
        OTP_TTL=300
        MAX_ATTEMPTS=5
        otp_key = f"otp:code:{key}"
        attempts_key = f"otp:attempts:{key}"
        otp_hash = cache.get(otp_key)
        print(f"Verifying OTP for {otp_key}: entered {entered_otp}, stored hash {otp_hash}")
        

        if not otp_hash:
            return False, "OTP expired"

        attempts = cache.get(
            attempts_key,
            0
        )

        if attempts >= MAX_ATTEMPTS:
            cache.delete_many([
                otp_key,
                attempts_key
            ])
            return False, "Too many attempts"

        if not check_password(
            entered_otp,
            otp_hash
        ):
            try:
                cache.incr(attempts_key)
            except ValueError:
                cache.set(
                    attempts_key,
                    1,
                    timeout=OTP_TTL
                )
            return False, "Invalid OTP"

        cache.delete_many([
            otp_key,
            attempts_key
        ])
        return True, "OTP verified"
