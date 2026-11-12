ROLE_PROFILES = {
    "ceo": {
        "department": "Leadership",
        "headline": "Company overview",
        "description": "Monitor the business, review department performance and handle key decisions.",
        "focus": ["Company performance", "Department health", "Pending approvals", "Business priorities"],
        "quick_actions": ["Review company report", "View department performance", "Review approvals"]
    },
    "founder": {
        "department": "Leadership",
        "headline": "Company overview",
        "description": "Monitor the business, review department performance and handle key decisions.",
        "focus": ["Company performance", "Department health", "Pending approvals", "Business priorities"],
        "quick_actions": ["Review company report", "View department performance", "Review approvals"]
    },
    "hr manager": {
        "department": "HR",
        "headline": "People & HR overview",
        "description": "Manage employee information, recruitment, leave and people operations.",
        "focus": ["Employee directory", "Recruitment pipeline", "Leave & attendance", "HR approvals"],
        "quick_actions": ["View employees", "Review leave requests", "Open recruitment"]
    },
    "finance manager": {
        "department": "Finance",
        "headline": "Finance overview",
        "description": "Keep track of financial operations, expenses, invoices and approvals.",
        "focus": ["Invoices", "Expense claims", "Payment approvals", "Financial reports"],
        "quick_actions": ["Review invoices", "Review expenses", "Open financial reports"]
    },
    "cto": {
        "department": "Software Development",
        "headline": "Engineering overview",
        "description": "Monitor development work, delivery progress, technical issues and releases.",
        "focus": ["Project progress", "Sprint activity", "Bugs & issues", "Release readiness"],
        "quick_actions": ["View projects", "Review open issues", "Check release activity"]
    },
    "operations manager": {
        "department": "Vehicle Operations",
        "headline": "Operations overview",
        "description": "Coordinate fleet activity, maintenance work and operational performance.",
        "focus": ["Fleet activity", "Maintenance queue", "Charging operations", "Operational reports"],
        "quick_actions": ["View fleet summary", "Review maintenance", "Open operations report"]
    },
    "support manager": {
        "department": "Customer Support",
        "headline": "Customer support overview",
        "description": "Manage support workload, escalations, response quality and team activity.",
        "focus": ["Open support tickets", "Escalations", "Team workload", "Response performance"],
        "quick_actions": ["View ticket queue", "Review escalations", "Open support report"]
    },
    "sales & marketing head": {
        "department": "Sales & Marketing",
        "headline": "Sales & marketing overview",
        "description": "Track leads, campaigns, customer activity and team performance.",
        "focus": ["Sales pipeline", "New leads", "Campaign activity", "Marketing reports"],
        "quick_actions": ["View leads", "Review campaigns", "Open sales report"]
    },
    "it head": {
        "department": "IT Administration",
        "headline": "IT & systems overview",
        "description": "Monitor company systems, access requests, infrastructure and security events.",
        "focus": ["System health", "Access requests", "Security alerts", "Integration status"],
        "quick_actions": ["View system status", "Review access requests", "Open audit activity"]
    }
}

def build_role_view(config, role_name):
    roles = config.get("roles", [])
    role = next(
        (r for r in roles if str(r.get("name", "")).casefold() == role_name.casefold()),
        {"name": role_name, "department": "General"}
    )

    key = role_name.strip().casefold()
    profile = ROLE_PROFILES.get(key, {})
    department = role.get("department") or profile.get("department", "General")
    if department == "General" and profile.get("department"):
        department = profile["department"]

    is_leadership = key in {"ceo", "founder", "owner", "admin"}
    departments = config.get("departments", [])
    if is_leadership:
        visible_departments = departments
    else:
        visible_departments = [
            d for d in departments
            if str(d.get("name", "")).casefold() == str(department).casefold()
        ]

    def belongs_to_role_department(item):
        item_department = str(item.get("department", "")).casefold()
        return is_leadership or item_department == str(department).casefold()

    workflows = [w for w in config.get("workflows", []) if belongs_to_role_department(w)]
    assistants = [a for a in config.get("ai_assistants", []) if belongs_to_role_department(a)]
    dashboard = next(
        (d for d in config.get("dashboards", [])
         if str(d.get("role", "")).casefold() == key),
        {}
    )

    return {
        "company": config.get("company", {}),
        "role": role,
        "department_name": department,
        "department": visible_departments[0] if visible_departments else {},
        "departments": visible_departments,
        "workflows": workflows,
        "assistants": assistants,
        "widgets": dashboard.get("widgets") or profile.get(
            "focus",
            ["My tasks", "Team updates", "Department activity", "Notifications"]
        ),
        "focus": profile.get("focus", ["My tasks", "Team updates", "Department activity", "Notifications"]),
        "quick_actions": profile.get("quick_actions", ["View my tasks", "Open team updates"]),
        "headline": profile.get("headline", f"{department} workspace"),
        "description": profile.get("description", "Your team workspace and day-to-day work."),
        "integrations": config.get("integrations", []),
        "notifications": config.get("notifications", [])
    }
