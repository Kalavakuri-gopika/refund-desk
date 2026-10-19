# RefundDesk: AI Customer Support & Refund Dispute Resolver

> **RefundDesk resolves e-commerce customer support questions and return requests using store policies, auto-issues refunds under $25, and routes damaged goods or larger claims to human Store Owner sign-off.**
.

---

## 👥 The Two Human Roles
- **Support Specialist (`POD_USER`):** Reviews inbound tickets, monitors customer sentiment, and responds to general inquiries and shipping delays.
- **Store Owner / Finance Lead (`POD_ADMIN`):** Holds sole authority to release refunds $> \$25.00$ or approve damaged item write-offs through the **Approval Gate**.

---

## 🛡️ The Core Loop & Approval Gate
1. **Inbound Inquiry:** A customer emails or chats regarding an order.
2. **AI Policy & Sentiment Triage (`triage-agent`):** The agent cross-references the customer's message against `/knowledge/store_policies.md` and order records in the `orders` table.
3. **Branching Decision:**
   - **Instant Satisfaction Guarantee ($\le \$25.00$):** Automatically approved and credited via the `process_refund` function. Ticket marked `auto_resolved`.
   - **The Human Gate ($> \$25.00$ or Damaged Claim):** The workflow **halts execution at a FORM node** assigned to the Store Owner. No refund can be issued until the human clicks **"Authorize Refund"**.
   - **Tracking Inquiry:** Returns carrier name and real-time tracking scan status.
4. **Nightly Carrier Audit (`nightly-shipment-sweep`):** Runs autonomously every night at 11:00 PM to audit transit timestamps and flag stalled shipments ($>48$h) before customers get frustrated.

---

## 🚀 Quickstart: Run in 2 Minutes

### 1. Prerequisites
Ensure you have the Lemma CLI installed and connected to your local stack:
```bash
uv tool install lemma-terminal
lemma auth login
```

### 2. Create Pod & Import Bundle
```bash
# Create pod shell
lemma pods create refund-desk --description "AI Customer Support & Dispute Operations"

# Import all tables, functions, agents, workflows, schedules, and app
lemma pods import ./refund-desk
```

### 3. Seed Realistic 30-Day Data
```bash
# Run the seed script (Linux/macOS)
./refund-desk/seed/seed.sh

# Or on Windows PowerShell:
.\refund-desk\seed\seed.ps1
```

### 4. Launch the Operations App
```bash
lemma apps deploy refund-desk-app ./refund-desk/apps/refund-desk-app/index.html
lemma apps open refund-desk-app
```

---


## 📦 Pod Resources Summary

| Resource | Type | Purpose |
| :--- | :--- | :--- |
| `orders` | Table (`shared`) | 30-day synthetic dataset of e-commerce orders, carriers, tracking, and refund statuses. |
| `tickets` | Table (`shared`) | Customer inquiries, triage classification, sentiment, and resolution history. |
| `/knowledge/store_policies.md` | File (RAG) | Official return windows, instant refund thresholds ($25), and damage guidelines. |
| `/knowledge/email_templates.md` | File (RAG) | Customer service reply templates. |
| `process_refund` | Function (Python) | Deterministic financial ledger write and ticket updater. |
| `audit_delayed_shipments` | Function (Python) | Audits carrier transit events for stalled packages. |
| `triage-agent` | Agent | Evaluates incoming messages against policy and determines routing. |
| `handle-inquiry` | Workflow | The end-to-end orchestration graph featuring the Store Owner FORM gate. |
| `nightly-shipment-sweep` | Schedule | Cron job running autonomous scans at 11:00 PM. |
| `refund-desk-app` | App | Single-page operations hub (Approval Inbox, Queue, Orders, Simulator). |

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.
