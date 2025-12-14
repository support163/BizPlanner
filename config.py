"""
a2v2.ai Business Plan Configuration - 2026
Product lines, pricing, and company parameters
"""

# Company Information
COMPANY = {
    "name": "a2v2.ai",
    "founded": 2024,
    "industry": "AI-Powered Healthcare Technology",
    "target_valuation": 10_000_000,  # $10M exit target
    "valuation_multiple": 4,  # Typical SaaS multiple (3-5x ARR)
}

# Product Lines with detailed metrics
PRODUCT_LINES = [
    {
        "name": "Pay For Access",
        "price": 4.99,
        "cogs": 3.99,
        "margin": 1.00,
        "margin_pct": 0.20,
        "current_units": 0,
        "type": "transactional",
        "description": "One-time AI consultation access",
        "growth_potential": "high",
        "target_market": "Casual users seeking quick health insights",
    },
    {
        "name": "Subscription Module",
        "price": 19.99,
        "cogs": 2.00,
        "margin": 17.99,
        "margin_pct": 0.90,
        "current_units": 0,
        "type": "subscription",
        "description": "Basic AI health monitoring subscription",
        "growth_potential": "very_high",
        "target_market": "Health-conscious individuals, basic wellness tracking",
    },
    {
        "name": "Subscription Concierge Medicine",
        "price": 39.99,
        "cogs": 4.00,
        "margin": 35.99,
        "margin_pct": 0.90,
        "current_units": 0,
        "type": "subscription",
        "description": "Premium AI-powered concierge health services",
        "growth_potential": "very_high",
        "target_market": "Premium users wanting personalized AI health guidance",
    },
    {
        "name": "Enterprise Subscription",
        "price": 499.00,
        "cogs": 49.90,
        "margin": 449.10,
        "margin_pct": 0.90,
        "current_units": 0.7,
        "type": "subscription",
        "description": "Enterprise-level AI health platform",
        "growth_potential": "high",
        "target_market": "Companies, clinics, healthcare organizations",
    },
    {
        "name": "Engineering Services",
        "price": 25.00,
        "cogs": 0.00,
        "margin": 25.00,
        "margin_pct": 1.00,
        "current_units": 225,
        "type": "service",
        "description": "Custom AI integration and development services",
        "growth_potential": "moderate",
        "target_market": "Healthcare providers needing custom AI solutions",
    },
]

# Exit Strategy Parameters
EXIT_STRATEGY = {
    "target_valuation": 10_000_000,
    "min_arr_for_exit": 2_500_000,  # At 4x multiple
    "ideal_arr_for_exit": 3_000_000,  # Some premium
    "target_months": 18,  # Aggressive 18-month timeline
    "buyer_types": [
        "Strategic Healthcare Acquirer",
        "Private Equity (Healthcare Focus)",
        "Larger AI/Tech Platform",
        "Healthcare System / Hospital Network",
    ],
}

# Growth Assumptions
GROWTH_ASSUMPTIONS = {
    "customer_acquisition_cost": 50,  # Average CAC
    "lifetime_value_months": 24,  # Average customer lifetime
    "churn_rate_monthly": 0.05,  # 5% monthly churn
    "viral_coefficient": 1.2,  # Each customer brings 0.2 additional
    "conversion_rate_free_to_paid": 0.03,  # 3% conversion
    "conversion_rate_basic_to_premium": 0.15,  # 15% upgrade rate
    "enterprise_close_rate": 0.10,  # 10% of qualified leads
}

# Operating Expenses (Monthly)
OPERATING_EXPENSES = {
    "salaries": 25000,  # Small team initially
    "cloud_infrastructure": 3000,
    "marketing": 5000,
    "legal_compliance": 2000,
    "office_misc": 1000,
    "software_tools": 500,
}

# Funding Milestones
FUNDING_MILESTONES = [
    {
        "stage": "Pre-Seed",
        "amount": 250_000,
        "valuation": 1_000_000,
        "trigger": "MVP + First 100 paying users",
    },
    {
        "stage": "Seed",
        "amount": 750_000,
        "valuation": 3_000_000,
        "trigger": "$50K MRR + Product-Market Fit",
    },
    {
        "stage": "Series A / Exit",
        "amount": 2_000_000,
        "valuation": 10_000_000,
        "trigger": "$200K+ MRR + Growth Metrics",
    },
]
