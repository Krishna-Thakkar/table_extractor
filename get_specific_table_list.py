intent_table_selector = [
    {
        "intent": "asset_details",
        "table_names": ["asset", "asset_history", "asset_type", "employee", "device_information", "device_information_history"]
    },
    {
        "intent": "attendance_details",
        "table_names": ["attendance_event", "attendance_regularization", "employee"]
    },
    {
        "intent": "interview_details",
        "table_names": ["candidates", "interview", "interview_resource", "job_interview", "jobs", "employee", "states"]
    },
    {
        "intent": "company_document_details",
        "table_names": ["company_document", "company_document_category"]
    },
    {
        "intent": "css_details",
        "table_names": ["css_files", "css_request_signed", "leads"]
    },
    {
        "intent": "deals_details",
        "table_names": ["deal_details", "deal_history", "deals", "employee", "leads", "currency"]
    },
    {
        "intent": "employee_details",
        "table_names": ["department_type", "designation_type", "employee", "employee_address",
                        "employee_education_type", "employee_emergency_contact", "employee_experience",
                        "employee_qualification", "employee_external_link", "states"]
    },
    {
        "intent": "team_details",
        "table_names": ["department_type", "designation_type", "employee", "employee_occupancy", "employee_skill",
                        "employee_skill_type", "employee_experience", "daily_allocation"]
    },
    {
        "intent": "invoice_details",
        "table_names": ["invoice", "invoice_histories", "invoice_payment_histories", "invoice_payments",
                        "project_basic", "employee", "project_resource"]
    },
    {
        "intent": "issue_details",
        "table_names": ["issue", "issue_work_log", "employee", "bucket_billing", "attendance_event"]
    },
    {
        "intent": "leads_details",
        "table_names": ["lead_details", "lead_follow_ups", "lead_history", "leads", "employee",
                        "project_client_company", "project_basic", "deals", "currency"]
    },
    {
        "intent": "leave_and_wfh_details",
        "table_names": ["leave_application", "leave_application_history", "leave_balance", "leave_balance_history",
                        "leave_type", "employee", "wfh_application", "holiday"]
    },
    {
        "intent": "lunch_details",
        "table_names": ["lunch_menu", "lunch_report", "employee"]
    },
    {
        "intent": "project_details",
        "table_names": ["project_basic", "project_change_request", "project_client_company", "project_document",
                        "project_escalation", "project_general_updates", "project_milestone", "project_resource",
                        "employee", "bucket_billing", "currency"]
    },
    {
        "intent": "sprint_details",
        "table_names": ["project_basic", "sprint", "sprint_issue", "issue", "employee"]
    },
]
