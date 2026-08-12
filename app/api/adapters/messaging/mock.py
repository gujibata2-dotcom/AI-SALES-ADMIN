from dataclasses import dataclass

@dataclass(frozen=True)
class MockAdapterResult:
    status: str
    result_reference: str

class MockMessagingAdapter:
    def send_message(self, target_reference: str, content_reference: str) -> MockAdapterResult:
        return MockAdapterResult("ACTION_EXECUTED", f"mock-message:{target_reference}")
    def get_message(self, message_reference: str) -> MockAdapterResult:
        return MockAdapterResult("ACTION_EXECUTED", f"mock-message-read:{message_reference}")
    def get_conversation(self, conversation_reference: str) -> MockAdapterResult:
        return MockAdapterResult("ACTION_EXECUTED", f"mock-conversation:{conversation_reference}")
    def check_delivery_status(self, message_reference: str) -> MockAdapterResult:
        return MockAdapterResult("ACTION_EXECUTED", f"mock-delivery:{message_reference}")
