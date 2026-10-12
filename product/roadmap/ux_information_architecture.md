# PalGen UX Information Architecture — Campaign Now, Leads Later

**Date:** 12 October 2026
**Status:** Design contract. Screens are illustrative; the structure and rules are binding.

## 1. Goal

Ship Campaign Management without a navigation, naming, or data-display redesign when Lead Management arrives. The UX must feel like **one marketing workspace** that gains modules, not a campaign tool with a bolted-on CRM.

## 2. Principles

1. **Contacts are the spine.** Campaigns, conversations, and (later) leads and ads all point at the same contact record and timeline.
2. **Channels are connections, not features.** Every channel and, later, every ad account lives in one Connections hub with one status vocabulary.
3. **Money is always visible and always separate.** Credits (communication), subscription, and (later) ad spend are shown as different things.
4. **Modules appear by entitlement.** Unpurchased or unavailable modules show as a clear, honest state, never as broken screens.
5. **Honest status.** Use one vocabulary everywhere: *Not connected · Needs authorization · Pending approval · Out of credits · Paused · Failed · Active.*
6. **Calm by default.** Pal and alerts appear only when severity and freshness justify it.

## 3. Navigation structure

```
Home (dashboard)
Campaigns            ← Campaign Management (available)
  Campaigns · Templates · Audiences · Reports
Inbox                ← conversations across channels (Phase 5)
Contacts             ← shared record; later gains Lead stage, pipeline views
Leads                ← reserved; "Lead Management — coming soon / not enabled"
  (later) Pipeline · Landing pages · Content · Attribution
Ads                  ← reserved
  (later) Meta Ads · Google Ads
Search & SEO         ← reserved (later: SEO · AEO)
Developers           ← reserved (later: API keys · Logs · Webhooks · Docs · Sandbox)
Reports              ← cross-module; campaign reports today, funnel later
Connections          ← channels now; ad accounts later
Wallet & Billing     ← credits per channel, invoices, subscription
Settings             ← team, roles, consent defaults, API keys
```

Rules:
- Reserved items are hidden or shown as a locked/"not enabled" state by entitlement; they are not built screens.
- The sidebar is generated from the module registry, not hard-coded per release.
- Campaign is a top-level area, not the app's identity. App chrome, home, and reports use neutral terms ("marketing", "contacts", "activity").

## 4. Shared surfaces designed for both modules

| Surface | Today (Campaign Management) | Later (Lead Management) |
|---|---|---|
| **Contacts list/detail** | Fields, tags, consent per channel, message timeline | Lifecycle stage, source, owner, score, ad/page touchpoints in the same timeline |
| **Audience builder** | Filter on tags, fields, channel consent, past engagement | Add filters on lead stage, source, campaign/ad attribution — same builder |
| **Contact timeline** | Sent, delivered, read, replied, opted out | Page view, form fill, ad click, stage change |
| **Connections hub** | WhatsApp, SMS, email domain, Instagram, phone | Meta and Google ad accounts, site/pixel connection |
| **Wallet** | Per-channel credit balances, recharge, usage statement | Ad spend shown as read-only *reference*, never as PalGen credit |
| **Reports** | Delivery and campaign performance | Funnel: ad → page → lead → campaign → reply → outcome |
| **Message log and usage** | Log and usage statement by campaign and channel, each row showing its source | Same log filterable by API key and source (campaign, inbox, API) |
| **Pal** | Low credits, template rejected, reply waiting | New lead, ad budget pacing, landing-page drop |
| **Entitlements/upsell** | Channel and module activation | Lead Management activation, with dependency explanation |

## 5. Key flows (Campaign Management)

1. **Connect a channel:** Connections → choose channel → guided provider steps → status moves to *Active* or a named blocking state with a next action.
2. **Recharge:** Wallet → choose channel → amount → payment → ledger entry appears → balance updates. Failed or pending payment is shown, not hidden.
3. **Build a campaign:** pick channel(s) → audience → template (approval status visible) → schedule/throttle → budget cap → cost estimate → confirm → run → live status.
4. **Handle replies:** Inbox → assign → respond within the channel's allowed window; opt-out handled automatically and visibly.

Each flow shows what blocks it (not connected, template pending, out of credits) before the user fills a long form.

## 6. Design rules that protect the lead roadmap

- No screen may label a contact as "customer" or "subscriber" in a way that excludes a lead. Use **contact**.
- No campaign table may be the only place a message or attribution is stored; events live on the contact timeline.
- Reports take a *scope* (campaign, channel, contact set, later source or ad) rather than being campaign-only.
- Terms for money are fixed: **Credits** (communication), **Plan** (subscription), **Ad spend** (paid to Google/Meta). Never "balance" without a qualifier.
- New navigation items are added through the module registry and need a design review for naming conflicts.
- Message logs and usage statements carry a **source** (campaign, inbox, later API key) from the first release.
- Pricing is pay-as-you-go: show a cost estimate before any send, and per-unit cost in every usage statement.

## 7. Pal in the UX

Pal is an optional layer over the same events. On web it is a compact capsule that expands to a card with at most two actions; on mobile or desktop surfaces it can mirror those cards. Operational screens stay free of chat; conversational help lives in a separate support/help drawer. Details in `pal_brainstorm.md` and `pal_apple_hig_ui_ux_analysis.md`.

## 8. Accessibility and platform

Keyboard navigation, screen-reader labels, reduced motion, responsive layouts, and non-Apple platforms are requirements for the web app. Apple-specific surfaces (Dynamic Island, notch) are optional later clients, not the primary UI.

## 9. Open UX questions

- Is the Inbox a top-level area from the first release, or is it shown inside Campaigns until more channels exist?
- How are multi-channel campaigns presented when channels have different template and window rules?
- Will agencies need multi-workspace switching early (client accounts)?
- Does the developer area live in the main workspace or in a separate developer portal?
