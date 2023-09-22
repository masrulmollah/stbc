import streamlit as st
from scipy.optimize import newton

def calculate_npv(rate, cashflows):
    npv = sum(cashflow / (1 + rate) ** i for i, cashflow in enumerate(cashflows))
    return npv

def calculate_irr(cashflows):
    try:
        def npv_eq(rate, cashflows):
            return sum(cashflow / (1 + rate) ** i for i, cashflow in enumerate(cashflows) if cashflow != 0)

        irr = newton(npv_eq, 0.1, args=(cashflows,))
        return round(irr * 100, 2)
    
    except RuntimeError:
        return None

def calculate_payback_period(cashflows):
    cumulative_cashflows = 0
    payback_period = 0
    
    for i, cashflow in enumerate(cashflows):
        cumulative_cashflows += cashflow
        if cumulative_cashflows >= 0:
            payback_period = i + (cumulative_cashflows - cashflow) / (cashflow if cashflow != 0 else 1)
            break
    
    return round(payback_period, 2)

def main():
    st.title("KGF Business Case APP")

    # Get user inputs
    one_year_cashflow = st.number_input("Enter the cash flow for the first year: ", min_value=0.0)
    capital_investment = st.number_input("Enter the capital investment: ", min_value=0.0)

    # Assuming a 12% discount rate
    discount_rate = 0.12

    # Calculate cash flows for the next four years with 7% inflation
    inflation_rate = 0.07
    cashflows = [-capital_investment] + [one_year_cashflow * (1 + inflation_rate) ** i for i in range(5)]

    # Calculate NPV, IRR, and Payback Period
    npv = calculate_npv(discount_rate, cashflows)
    irr = calculate_irr(cashflows)
    payback_period = calculate_payback_period(cashflows)

    st.write(f"Net Present Value (NPV): BDT {npv:.2f}")
    
    if irr is not None:
        st.write(f"Internal Rate of Return (IRR): {irr:.2f}%")
    else:
        st.write("Internal Rate of Return (IRR) could not be calculated.")
    
    st.write(f"Payback Period: {payback_period} years")

if __name__ == "__main__":
    main()
