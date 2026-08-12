class MockPaymentAdapter:
    def get_payment_status(self, payment_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-payment-status:{payment_reference}"}
    def prepare_payment(self, payment_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-payment-prepared:{payment_reference}"}
    def verify_payment(self, payment_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-payment-verified:{payment_reference}"}
    def process_payment(self, *_args, **_kwargs): raise RuntimeError("PROCESS_PAYMENT is blocked in Phase 10")
    def refund_payment(self, *_args, **_kwargs): raise RuntimeError("REFUND_PAYMENT is blocked in Phase 10")
    def charge_payment(self, *_args, **_kwargs): raise RuntimeError("CHARGE_PAYMENT is blocked in Phase 10")
