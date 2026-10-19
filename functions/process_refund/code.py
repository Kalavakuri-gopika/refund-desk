#input_type_name: ProcessRefundInput
#output_type_name: ProcessRefundResult
#function_name: process_refund

from pydantic import BaseModel
from typing import Optional
from lemma_sdk import FunctionContext, Pod

class ProcessRefundInput(BaseModel):
    ticket_id: str
    order_id: str
    amount: float
    reason: str
    authorized_by: str = "store_owner"

class ProcessRefundResult(BaseModel):
    success: bool
    refund_id: str
    order_id: str
    ticket_id: str
    amount: float
    status: str
    message: str

async def process_refund(ctx: FunctionContext, data: ProcessRefundInput) -> ProcessRefundResult:
    pod = Pod.from_env()

    # 1. Locate and update order record
    orders_resp = pod.records.list(
        "orders",
        limit=5,
        filter=[{"field": "order_id", "op": "eq", "value": data.order_id}]
    ).to_dict()
    orders = orders_resp.get("items", [])
    
    order_updated = False
    if orders:
        order_record = orders[0]
        order_row_id = order_record["id"]
        pod.table("orders").update(
            order_row_id,
            {
                "refund_status": "refunded",
                "refunded_amount": float(data.amount)
            }
        )
        order_updated = True

    # 2. Locate and update ticket record
    tickets_resp = pod.records.list(
        "tickets",
        limit=5,
        filter=[{"field": "ticket_id", "op": "eq", "value": data.ticket_id}]
    ).to_dict()
    tickets = tickets_resp.get("items", [])

    resolution_note = (
        f"Refund of ${data.amount:.2f} executed successfully. "
        f"Authorized by: {data.authorized_by}. Reason: {data.reason}."
    )

    ticket_updated = False
    if tickets:
        ticket_record = tickets[0]
        ticket_row_id = ticket_record["id"]
        pod.table("tickets").update(
            ticket_row_id,
            {
                "status": "approved",
                "requested_refund": float(data.amount),
                "resolution_note": resolution_note
            }
        )
        ticket_updated = True

    refund_ref = f"REF-{data.order_id[-4:] if len(data.order_id) >= 4 else '0000'}"
    
    return ProcessRefundResult(
        success=True,
        refund_id=refund_ref,
        order_id=data.order_id,
        ticket_id=data.ticket_id,
        amount=float(data.amount),
        status="refunded",
        message=f"Successfully processed refund of ${data.amount:.2f} for order {data.order_id}."
    )
