#!/usr/bin/env python3
"""
a2v2.ai Business Plan 2026 - Main Application
Generates business plan documents and financial projections
"""

import os
import json
import webbrowser
from pathlib import Path

from config import COMPANY, PRODUCT_LINES, EXIT_STRATEGY
from projections import generate_all_scenarios, export_projections_json, find_exit_timeline
from business_plan import generate_full_business_plan


def print_header():
    """Print application header"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    a2v2.ai BUSINESS PLAN 2026                                ║
║                    Path to $10M Exit Valuation                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)


def print_product_chart():
    """Print the completed product lines chart"""
    print("\n" + "=" * 80)
    print("PRODUCT LINES ANALYSIS - COMPLETED CHART")
    print("=" * 80)
    print(f"\n{'Product Lines':<35} {'Units/Mo':>10} {'Price':>12} {'COGS':>10} {'Margin':>12}")
    print("-" * 80)

    for product in PRODUCT_LINES:
        print(f"{product['name']:<35} {product['current_units']:>10.1f} ${product['price']:>10.2f} ${product['cogs']:>8.2f} ${product['margin']:>10.2f}")

    # Calculate totals
    total_current_revenue = sum(p['price'] * p['current_units'] for p in PRODUCT_LINES)
    total_current_margin = sum(p['margin'] * p['current_units'] for p in PRODUCT_LINES)

    print("-" * 80)
    print(f"{'CURRENT MONTHLY TOTALS':<35} {'':<10} ${total_current_revenue:>10.2f} {'':<10} ${total_current_margin:>10.2f}")
    print()


def print_exit_analysis():
    """Print $10M exit analysis"""
    print("\n" + "=" * 80)
    print("PATH TO $10M EXIT - SCENARIO ANALYSIS")
    print("=" * 80)

    scenarios = generate_all_scenarios()

    for name, scenario in scenarios.items():
        exit_info = find_exit_timeline(scenario.projections)

        print(f"\n{scenario.name.upper()}")
        print(f"  Monthly Growth Rate: {scenario.monthly_growth_rate * 100:.0f}%")
        print("-" * 40)

        if exit_info["achievable"]:
            print(f"  ✓ $10M EXIT ACHIEVABLE")
            print(f"  Timeline: {exit_info['months_to_exit']} months")
            print(f"  Exit Date: {exit_info['exit_month']}/{exit_info['exit_year']}")
            print(f"  Final MRR: ${exit_info['final_mrr']:,.0f}")
            print(f"  Final ARR: ${exit_info['final_arr']:,.0f}")
            print(f"  Subscribers: {exit_info['total_subscribers']:,}")
        else:
            print(f"  ✗ Extended timeline required")
            print(f"  24-Month Valuation: ${exit_info['final_valuation']:,.0f}")
            print(f"  Gap to $10M: ${exit_info['gap_to_target']:,.0f}")
            print(f"  Final MRR: ${exit_info['final_mrr']:,.0f}")
            print(f"  Subscribers: {exit_info['total_subscribers']:,}")


def print_key_recommendations():
    """Print key strategic recommendations"""
    print("\n" + "=" * 80)
    print("KEY STRATEGIC RECOMMENDATIONS")
    print("=" * 80)

    recommendations = """
1. PRIORITIZE HIGH-MARGIN SUBSCRIPTIONS
   - Focus on $19.99 and $39.99 tiers (90% gross margin)
   - Target: 80% of revenue from recurring subscriptions
   - Engineering services for cash flow, not growth

2. AGGRESSIVE ENTERPRISE SALES
   - Each $499/month account = 25 basic subscribers equivalent
   - Target: 100+ enterprise accounts by end of 2026
   - Build dedicated enterprise sales team by Q2 2025

3. PRODUCT-LED GROWTH STRATEGY
   - Use Pay-For-Access ($4.99) as top-of-funnel
   - Target 10% conversion to monthly subscription
   - Build referral program with viral coefficient > 1.2

4. UNIT ECONOMICS TARGETS
   - CAC: <$50 for consumer, <$500 for enterprise
   - LTV:CAC ratio: >10:1 (currently 12:1)
   - Churn: <5% monthly for basic, <2% for enterprise

5. EXIT PREPARATION (Starting Q1 2026)
   - Clean financial records (GAAP compliant)
   - Customer contracts organized
   - Data room preparation
   - Engage investment banker

6. MILESTONE-BASED FUNDRAISING
   - Pre-Seed ($250K): MVP + 100 users → Q1 2025
   - Seed ($750K): $50K MRR + PMF → Q3 2025
   - Exit/Series A: $200K+ MRR → Q3 2026
    """
    print(recommendations)


def generate_all_outputs():
    """Generate all output files"""
    print("\nGenerating output files...")

    # Generate full business plan
    plan = generate_full_business_plan()
    with open("A2V2_Business_Plan_2026.txt", "w") as f:
        f.write(plan)
    print("  ✓ A2V2_Business_Plan_2026.txt")

    # Generate projections JSON
    scenarios = generate_all_scenarios()
    json_data = export_projections_json(scenarios)
    with open("projections_data.json", "w") as f:
        f.write(json_data)
    print("  ✓ projections_data.json")

    # Check if dashboard exists
    if Path("dashboard.html").exists():
        print("  ✓ dashboard.html (interactive visualization)")

    print("\nAll files generated successfully!")


def main():
    """Main application entry point"""
    print_header()
    print_product_chart()
    print_exit_analysis()
    print_key_recommendations()
    generate_all_outputs()

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("""
1. Open dashboard.html in your browser to explore interactive projections
2. Review A2V2_Business_Plan_2026.txt for the complete business plan
3. Use projections_data.json for integration with other tools

To open the dashboard, run:
    python -m http.server 8000

Then visit: http://localhost:8000/dashboard.html
    """)


if __name__ == "__main__":
    main()
