class MockEcommerceAdapter:
    def get_product(self, product_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-product:{product_reference}"}
    def get_price(self, product_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-price:{product_reference}"}
    def get_stock(self, product_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-stock:{product_reference}"}
    def prepare_order(self, order_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-order-prepared:{order_reference}"}
    def get_order_status(self, order_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-order-status:{order_reference}"}
