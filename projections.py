"""
a2v2.ai Financial Projections Engine
Models growth scenarios and path to $10M valuation
"""

from dataclasses import dataclass, field
from typing import List, Dict
import json
from config import (
    PRODUCT_LINES,
    EXIT_STRATEGY,
    GROWTH_ASSUMPTIONS,
    OPERATING_EXPENSES,
)


@dataclass
class MonthlyProjection:
    """Single month financial projection"""
    month: int
    year: int

    # Revenue by product
    pay_access_units: int = 0
    subscription_basic_units: int = 0
    subscription_concierge_units: int = 0
    enterprise_units: float = 0
    engineering_hours: int = 0

    # Financials
    gross_revenue: float = 0
    cogs: float = 0
    gross_profit: float = 0
    operating_expenses: float = 0
    net_income: float = 0

    # Key Metrics
    mrr: float = 0
    arr: float = 0
    total_subscribers: int = 0
    new_subscribers: int = 0
    churned_subscribers: int = 0

    # Valuation
    implied_valuation: float = 0


@dataclass
class GrowthScenario:
    """Growth scenario with monthly projections"""
    name: str
    description: str
    monthly_growth_rate: float  # Monthly subscriber growth
    projections: List[MonthlyProjection] = field(default_factory=list)


def calculate_product_revenue(units: dict) -> dict:
    """Calculate revenue, COGS, and margin for given units"""
    products = {p["name"]: p for p in PRODUCT_LINES}

    revenue = {
        "pay_access": units.get("pay_access", 0) * products["Pay For Access"]["price"],
        "subscription_basic": units.get("subscription_basic", 0) * products["Subscription Module"]["price"],
        "subscription_concierge": units.get("subscription_concierge", 0) * products["Subscription Concierge Medicine"]["price"],
        "enterprise": units.get("enterprise", 0) * products["Enterprise Subscription"]["price"],
        "engineering": units.get("engineering", 0) * products["Engineering Services"]["price"],
    }

    cogs = {
        "pay_access": units.get("pay_access", 0) * products["Pay For Access"]["cogs"],
        "subscription_basic": units.get("subscription_basic", 0) * products["Subscription Module"]["cogs"],
        "subscription_concierge": units.get("subscription_concierge", 0) * products["Subscription Concierge Medicine"]["cogs"],
        "enterprise": units.get("enterprise", 0) * products["Enterprise Subscription"]["cogs"],
        "engineering": units.get("engineering", 0) * products["Engineering Services"]["cogs"],
    }

    return {
        "total_revenue": sum(revenue.values()),
        "total_cogs": sum(cogs.values()),
        "gross_profit": sum(revenue.values()) - sum(cogs.values()),
        "revenue_breakdown": revenue,
        "cogs_breakdown": cogs,
    }


def project_month(
    month: int,
    prev_projection: MonthlyProjection,
    growth_rate: float,
    scenario_type: str = "balanced"
) -> MonthlyProjection:
    """Project a single month based on previous month and growth assumptions"""

    churn = GROWTH_ASSUMPTIONS["churn_rate_monthly"]
    upgrade_rate = GROWTH_ASSUMPTIONS["conversion_rate_basic_to_premium"]

    # Calculate subscriber growth
    prev_basic = prev_projection.subscription_basic_units
    prev_concierge = prev_projection.subscription_concierge_units
    prev_enterprise = prev_projection.enterprise_units

    # Apply churn
    churned_basic = int(prev_basic * churn)
    churned_concierge = int(prev_concierge * churn * 0.7)  # Lower churn for premium
    churned_enterprise = prev_enterprise * churn * 0.3  # Very low enterprise churn

    # Apply growth (new customers)
    if scenario_type == "aggressive":
        new_basic = int(prev_basic * growth_rate * 1.5) + 50
        new_concierge = int(prev_concierge * growth_rate * 1.3) + 20
        new_enterprise = prev_enterprise * growth_rate * 0.8 + 0.5
    elif scenario_type == "conservative":
        new_basic = int(prev_basic * growth_rate * 0.7) + 20
        new_concierge = int(prev_concierge * growth_rate * 0.5) + 5
        new_enterprise = prev_enterprise * growth_rate * 0.3 + 0.2
    else:  # balanced
        new_basic = int(prev_basic * growth_rate) + 35
        new_concierge = int(prev_concierge * growth_rate * 0.9) + 12
        new_enterprise = prev_enterprise * growth_rate * 0.5 + 0.3

    # Upgrades from basic to premium
    upgrades = int(prev_basic * upgrade_rate)

    # Calculate new totals
    basic_units = max(0, prev_basic - churned_basic - upgrades + new_basic)
    concierge_units = max(0, prev_concierge - churned_concierge + upgrades + new_concierge)
    enterprise_units = max(0, prev_enterprise - churned_enterprise + new_enterprise)

    # Pay for access (transactional - based on traffic/marketing)
    pay_access = int(50 + (basic_units + concierge_units) * 0.3 + month * 10)

    # Engineering services (steady with slight growth)
    engineering = int(225 + month * 5)

    # Calculate financials
    units = {
        "pay_access": pay_access,
        "subscription_basic": basic_units,
        "subscription_concierge": concierge_units,
        "enterprise": enterprise_units,
        "engineering": engineering,
    }

    financials = calculate_product_revenue(units)

    # Operating expenses (grow with company)
    base_opex = sum(OPERATING_EXPENSES.values())
    opex_multiplier = 1 + (month / 24) * 0.5  # Grow 50% over 24 months
    total_opex = base_opex * opex_multiplier

    # MRR from subscriptions only
    mrr = (
        basic_units * 19.99 +
        concierge_units * 39.99 +
        enterprise_units * 499.00
    )

    # Calculate projection
    year = 2025 + (month // 12)
    month_in_year = (month % 12) + 1

    return MonthlyProjection(
        month=month_in_year,
        year=year,
        pay_access_units=pay_access,
        subscription_basic_units=basic_units,
        subscription_concierge_units=concierge_units,
        enterprise_units=enterprise_units,
        engineering_hours=engineering,
        gross_revenue=financials["total_revenue"],
        cogs=financials["total_cogs"],
        gross_profit=financials["gross_profit"],
        operating_expenses=total_opex,
        net_income=financials["gross_profit"] - total_opex,
        mrr=mrr,
        arr=mrr * 12,
        total_subscribers=basic_units + concierge_units + int(enterprise_units),
        new_subscribers=new_basic + new_concierge + int(new_enterprise),
        churned_subscribers=churned_basic + churned_concierge + int(churned_enterprise),
        implied_valuation=mrr * 12 * 4,  # 4x ARR multiple
    )


def generate_projections(
    months: int = 24,
    scenario_type: str = "balanced",
    growth_rate: float = 0.15
) -> List[MonthlyProjection]:
    """Generate monthly projections for given period"""

    projections = []

    # Starting point (Month 0 - current state)
    initial = MonthlyProjection(
        month=1,
        year=2025,
        pay_access_units=0,
        subscription_basic_units=50,  # Starting base
        subscription_concierge_units=10,
        enterprise_units=1,
        engineering_hours=225,
        mrr=50 * 19.99 + 10 * 39.99 + 1 * 499.00,
    )
    initial.arr = initial.mrr * 12
    initial.implied_valuation = initial.arr * 4

    projections.append(initial)

    # Generate future months
    for month in range(1, months + 1):
        proj = project_month(
            month=month,
            prev_projection=projections[-1],
            growth_rate=growth_rate,
            scenario_type=scenario_type
        )
        projections.append(proj)

    return projections


def find_exit_timeline(projections: List[MonthlyProjection]) -> Dict:
    """Find when $10M valuation is achievable"""

    target = EXIT_STRATEGY["target_valuation"]
    min_arr = EXIT_STRATEGY["min_arr_for_exit"]

    for i, proj in enumerate(projections):
        if proj.implied_valuation >= target:
            return {
                "months_to_exit": i,
                "exit_month": proj.month,
                "exit_year": proj.year,
                "final_arr": proj.arr,
                "final_mrr": proj.mrr,
                "final_valuation": proj.implied_valuation,
                "total_subscribers": proj.total_subscribers,
                "achievable": True,
            }

    # If not achieved in projection period
    last = projections[-1]
    return {
        "months_to_exit": len(projections),
        "exit_month": last.month,
        "exit_year": last.year,
        "final_arr": last.arr,
        "final_mrr": last.mrr,
        "final_valuation": last.implied_valuation,
        "total_subscribers": last.total_subscribers,
        "achievable": False,
        "gap_to_target": target - last.implied_valuation,
    }


def generate_all_scenarios() -> Dict[str, GrowthScenario]:
    """Generate conservative, balanced, and aggressive scenarios"""

    scenarios = {}

    # Conservative: 10% monthly growth
    conservative_projections = generate_projections(
        months=24,
        scenario_type="conservative",
        growth_rate=0.10
    )
    scenarios["conservative"] = GrowthScenario(
        name="Conservative Growth",
        description="10% monthly growth, higher churn assumptions",
        monthly_growth_rate=0.10,
        projections=conservative_projections
    )

    # Balanced: 15% monthly growth
    balanced_projections = generate_projections(
        months=24,
        scenario_type="balanced",
        growth_rate=0.15
    )
    scenarios["balanced"] = GrowthScenario(
        name="Balanced Growth",
        description="15% monthly growth, moderate assumptions",
        monthly_growth_rate=0.15,
        projections=balanced_projections
    )

    # Aggressive: 25% monthly growth
    aggressive_projections = generate_projections(
        months=24,
        scenario_type="aggressive",
        growth_rate=0.25
    )
    scenarios["aggressive"] = GrowthScenario(
        name="Aggressive Growth",
        description="25% monthly growth, optimistic assumptions",
        monthly_growth_rate=0.25,
        projections=aggressive_projections
    )

    return scenarios


def export_projections_json(scenarios: Dict[str, GrowthScenario]) -> str:
    """Export projections to JSON for dashboard"""

    data = {}
    for name, scenario in scenarios.items():
        data[name] = {
            "name": scenario.name,
            "description": scenario.description,
            "growth_rate": scenario.monthly_growth_rate,
            "projections": [
                {
                    "month": p.month,
                    "year": p.year,
                    "label": f"{p.year}-{p.month:02d}",
                    "mrr": round(p.mrr, 2),
                    "arr": round(p.arr, 2),
                    "gross_revenue": round(p.gross_revenue, 2),
                    "net_income": round(p.net_income, 2),
                    "subscribers": p.total_subscribers,
                    "valuation": round(p.implied_valuation, 2),
                    "basic_subs": p.subscription_basic_units,
                    "concierge_subs": p.subscription_concierge_units,
                    "enterprise_subs": round(p.enterprise_units, 1),
                }
                for p in scenario.projections
            ],
            "exit_analysis": find_exit_timeline(scenario.projections),
        }

    return json.dumps(data, indent=2)


if __name__ == "__main__":
    # Generate all scenarios
    scenarios = generate_all_scenarios()

    print("=" * 60)
    print("a2v2.ai 2026 Business Plan - Financial Projections")
    print("=" * 60)

    for name, scenario in scenarios.items():
        print(f"\n--- {scenario.name} ({scenario.monthly_growth_rate*100:.0f}% monthly growth) ---")
        exit_info = find_exit_timeline(scenario.projections)

        if exit_info["achievable"]:
            print(f"  $10M Valuation achievable in: {exit_info['months_to_exit']} months")
            print(f"  Exit Date: {exit_info['exit_month']}/{exit_info['exit_year']}")
        else:
            print(f"  $10M not achieved in 24 months")
            print(f"  Gap to target: ${exit_info['gap_to_target']:,.0f}")

        print(f"  Final ARR: ${exit_info['final_arr']:,.0f}")
        print(f"  Final MRR: ${exit_info['final_mrr']:,.0f}")
        print(f"  Final Valuation: ${exit_info['final_valuation']:,.0f}")
        print(f"  Total Subscribers: {exit_info['total_subscribers']:,}")

    # Export for dashboard
    json_data = export_projections_json(scenarios)
    with open("projections_data.json", "w") as f:
        f.write(json_data)
    print("\n\nProjection data exported to projections_data.json")
