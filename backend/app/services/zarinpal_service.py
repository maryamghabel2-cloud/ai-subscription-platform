import requests
from fastapi import HTTPException
from app.config import settings


class ZarinpalService:
    """
    Service for handling Zarinpal payments
    """
    def __init__(self):
        self.merchant_id = settings.ZARINPAL_MERCHANT_ID
        self.sandbox = settings.ZARINPAL_SANDBOX
        self.base_url = (
            "https://sandbox.zarinpal.com/pg/services/WebGate/"
            if self.sandbox
            else "https://www.zarinpal.com/pg/services/WebGate/"
        )

    def create_payment(
        self, amount: int, description: str, callback_url: str, email: str = None, mobile: str = None
    ):
        """
        Create a new payment request
        amount: in Rials (1 Toman = 10 Rials)
        Returns: dict with authority and payment_url
        """
        data = {
            "MerchantID": self.merchant_id,
            "Amount": amount,
            "Description": description,
            "CallbackURL": callback_url,
        }

        if email:
            data["Email"] = email
        if mobile:
            data["Mobile"] = mobile

        try:
            response = requests.post(f"{self.base_url}pgRequest.json", json=data)
            result = response.json()

            if result.get("Status") == 100:
                return {
                    "authority": result["Authority"],
                    "payment_url": (
                        f"https://sandbox.zarinpal.com/pg/StartPay/{result['Authority']}"
                        if self.sandbox
                        else f"https://www.zarinpal.com/pg/StartPay/{result['Authority']}"
                    ),
                }
            else:
                status_messages = {
                    -1: "اطلاعات ارسالی ناقص می‌باشد",
                    -2: "IP و یا مرچنت کد پذیرنده صحیح نمی‌باشد",
                    -3: "با توجه به محدودیت‌های شاپرک امکان پرداخت با مبلغ درخواستی میسر نمی‌باشد",
                    -4: "سطح تایید پذیرنده پایین‌تر از سطح نقره می‌باشد",
                    -11: "درخواست مورد نظر یافت نشد",
                    -12: "امکان ویرایش درخواست میسر نمی‌باشد",
                    -21: "هنوز واریزی انجام نشده است",
                    -22: "تراکنش ناموفق می‌باشد",
                    -33: "مبلغ تراکنش با مبلغ پرداخت شده مطابقت ندارد",
                    -34: "سقف تراکنش از حد مجاز عبور نموده است",
                    -40: "اجازه دسترسی به متد مربوطه وجود ندارد",
                    -41: "اطلاعات ارسالی تکراری می‌باشد",
                    -54: "تراکنش مورد نظر یافت نشد",
                }
                raise HTTPException(
                    status_code=400,
                    detail=f"Zarinpal error {result.get('Status', 'Unknown')}: {status_messages.get(result.get('Status', 0), 'Unknown error')}"
                )
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500, detail=f"Payment gateway connection failed: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Payment creation failed: {str(e)}"
            )

    def verify_payment(self, authority: str, amount: int):
        """
        Verify payment after callback
        amount: in Rials
        Returns: dict with verification status
        """
        data = {
            "MerchantID": self.merchant_id,
            "Authority": authority,
            "Amount": amount,
        }

        try:
            response = requests.post(f"{self.base_url}pgVerification.json", json=data)
            result = response.json()

            if result.get("Status") == 100:
                return {
                    "success": True,
                    "ref_id": result["RefID"],
                    "card_pan": result.get("CardPan", "****"),
                    "card_hash": result.get("CardHash", ""),
                    "fee_type": result.get("FeeType", ""),
                    "fee": result.get("Fee", 0),
                }
            else:
                return {
                    "success": False,
                    "status": result.get("Status", -1),
                    "message": result.get("Message", "Unknown error"),
                }
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500, detail=f"Payment verification connection failed: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Payment verification failed: {str(e)}"
            )
