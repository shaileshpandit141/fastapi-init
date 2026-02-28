from secrets import randbelow

# =============================================================================
# Otp generator class.
# =============================================================================


class OtpGenerator:
    @staticmethod
    def generate(length: int = 6) -> str:
        if length < 1:
            raise ValueError("OTP length must be at least 1")

        return "".join(str(randbelow(10)) for _ in range(length))
