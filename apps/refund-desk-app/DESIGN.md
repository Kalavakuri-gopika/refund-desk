# RefundDesk App Design Specification

## Purpose & Persona
- **Purpose:** A dedicated operations hub for e-commerce customer support and refund governance. It connects customer tickets, shipment tracking, store return policies, and the Store Owner's financial approval gate into a single cohesive interface.
- **Target Personas:**
  1. **Support Specialist:** Monitors incoming inquiries, views AI policy classifications, and reviews delivery alerts.
  2. **Store Owner / Finance Lead:** Checks the Approval Inbox, verifies high-stakes claims ($> $25), and authorizes refunds.

## Page Map & Views
1. **Approval Inbox (`/approvals`):**
   - The primary decision gate: displays pending refund requests exceeding the $25 instant threshold.
   - Shows order value, purchase date, customer explanation, and AI policy audit.
   - Provides 1-click "Authorize Refund" and "Decline" actions.
2. **Support Ticket Queue (`/tickets`):**
   - Filterable stream of customer tickets (`All`, `New`, `Waiting Approval`, `Auto-Resolved`, `Closed`).
   - Visual sentiment tags (`frustrated`, `angry`, `neutral`, `positive`).
   - Detailed side drawer showing customer message, AI diagnosis, and resolution notes.
3. **Orders & Shipments (`/orders`):**
   - Searchable table of customer orders, tracking numbers, carriers (FedEx, UPS, DHL), and shipping status.
   - Visual badges for `Delivered`, `In Transit`, and `Delayed`.
4. **Interactive Simulator (`/simulate`):**
   - Live testing console with pre-configured customer email scenarios (e.g., "$18 auto-approved refund", "$85 damaged goods requiring owner approval", "Tracking inquiry").
   - Lets reviewers test the entire agentic loop and trigger the approval gate on camera.

## Design Aesthetics & Theme
- Built with an elegant, modern dark/light dual theme using a curated palette (rich slate, amber gold accents, emerald green approval indicators, crimson alerts).
- Smooth CSS micro-animations on approval action and live filter switches.
- Direct integration with Lemma Client SDK (`records.list`, `records.create`, `records.update`, `functions.run`).
