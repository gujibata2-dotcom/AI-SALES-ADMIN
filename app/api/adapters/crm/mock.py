class MockCRMAdapter:
    def get_customer(self, customer_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-customer:{customer_reference}"}
    def create_lead(self, lead_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-lead:{lead_reference}"}
    def update_lead(self, lead_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-lead-update:{lead_reference}"}
    def get_task(self, task_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-task:{task_reference}"}
    def create_task(self, task_reference: str): return {"status":"ACTION_EXECUTED","result_reference":f"mock-task-create:{task_reference}"}
