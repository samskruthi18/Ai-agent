# Three-person build checklist

## Person 1 — Onboarding and UI
- Capture company, size, departments, workflows, preferred tools, restricted data, and approval needs.
- Render generated blueprint for review and explicit approval.
- Show department workspaces and export blueprint JSON.

## Person 2 — Local Qwen planning
- Connect through LM Studio's OpenAI-compatible local endpoint.
- Convert intake to a compact, validated JSON blueprint.
- Keep generated recommendations separate from enforceable policy.

## Person 3 — Roles, policy, and audit
- Enforce department scope and role permissions in deterministic code.
- Deny sensitive operations that are not implemented.
- Log every workspace access and action decision to SQLite.

## Integration gates
- Agree the intake schema before parallel coding.
- Agree the blueprint JSON schema and stable policy function before UI integration.
- Review one allowed flow and one denied flow together.
- Demo with fictional company data and a local Qwen server only.
