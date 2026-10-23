# Preliminary Submission — Draft

**Team:** TODO — insert the official team name  
**Project:** Orbyte MessagePilot  
**Track / domain:** TODO — confirm the official category

## Problem

Customer-facing teams receive messages through several channels and need a consistent way to identify what deserves attention first.

## Proposed solution

Orbyte MessagePilot demonstrates a unified triage workflow. A deterministic rules module scores a normalized message using sender role and configured keywords, assigns a P1–P4 tier, and flags risk for human review. The HTML prototypes demonstrate a local inbox, editable reply drafts, approval/rejection, reassignment, and completion actions.

## Demonstration scope

All supplied messages are synthetic. Website actions are in-memory training simulations. The system does not connect to WhatsApp, email, Discord, or a live database, and cannot send messages. The RunPod handler is a separate triage-job entry point; it returns scores and a human-review flag.

## Current limitations

The scoring is a transparent keyword heuristic, not a trained AI model. The current files do not include a deployed RunPod endpoint, live channel integrations, or evidence of user testing. Add only verified claims and results before submission.
