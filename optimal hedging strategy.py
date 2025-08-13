import numpy as np
import pandas as pd
from scipy.optimize import minimize

def optimize_hedge_quantity(portfolio_pnl, stock_returns, capital_cost, max_cost=50000):

    """Optimize hedge quantity for a stock to maximize VaR improvement."""
    
    def objective(x):
        
        hedged_pnl = portfolio_pnl + x * stock_returns
        return np.percentile(hedged_pnl, 5)  # Returna the 95% VaR
    
    # Constraints: |x| * capital_cost <= max_cost
    constraints = ({'type': 'ineq', 'fun': lambda x: max_cost - abs(x) * capital_cost})
    
    # Bounds: Allowing both long and short positions
    bounds = [(-max_cost / capital_cost, max_cost / capital_cost)]
    
    # Optimizing to maximize VaR (minimize negative VaR)
    result = minimize(
        
        lambda x: -objective(x),  # Minimize negative VaR = Maximize VaR
        x0=0,  # Starting from no position
        bounds=bounds,
        constraints=constraints
    
    )
    
    if result.success:
        
        optimal_qty = int(np.round(result.x[0]))
        new_VaR = objective(optimal_qty)
        cost = abs(optimal_qty) * capital_cost
        improvement = np.percentile(portfolio_pnl, 5) - new_VaR
        return optimal_qty, new_VaR, cost, improvement
    
    return None

# Loading data
returns = pd.read_csv('stocks_returns.csv') / 100  # Convert % to decimals
metadata = pd.read_csv('stocks_metadata.csv')

# Parse input
input_data = input('Input: ').split()
portfolio_id = input_data[0]
portfolio_pnl = np.array([float(x) for x in input_data[1:]])

# Calculating original VaR
VaR_95 = np.percentile(portfolio_pnl, 5)
print(f"Original 95% VaR: {VaR_95:.2f}")

# Finding optimal hedges
potential_hedges = []
max_budget = 50000  # Adjust based on constraints

for stock_id in returns.columns:
    
    if stock_id == 'Date':
        continue
    
    stock_returns = returns[stock_id].dropna().values
    if len(stock_returns) < len(portfolio_pnl):
        continue
    
    stock_info = metadata[metadata['Stock_Id'] == stock_id]  # Matching the column name
    if stock_info.empty:
        continue
    
    capital_cost = stock_info['Capital_Cost'].values[0]
    aligned_returns = stock_returns[:len(portfolio_pnl)]
    
    # Optimizing quantity
    result = optimize_hedge_quantity(portfolio_pnl, aligned_returns, capital_cost, max_budget)
    
    if result:
        
        qty, new_VaR, cost, improvement = result
        if improvement > 0:  # Only to consider if it improves VaR
            
            potential_hedges.append({
                'stock_id': stock_id,
                'quantity': qty,
                'new_VaR': new_VaR,
                'cost': cost,
                'improvement': improvement,
                'cost_effectiveness': improvement / cost if cost > 0 else 0
            })

# Selecting the best hedges
if potential_hedges:
    
    # Sorting by cost-effectiveness (improvement per $ spent)
    potential_hedges.sort(key=lambda x: x['cost_effectiveness'], reverse=True)
    
    selected_hedges = []
    remaining_budget = max_budget
    
    for hedge in potential_hedges:
        
        if hedge['cost'] <= remaining_budget:
            
            selected_hedges.append(hedge)
            remaining_budget -= hedge['cost']
    
    # Printing results
    print("\nRecommended hedge positions:")
    for hedge in selected_hedges:
        print(f"{hedge['stock_id']} {hedge['quantity']}")
    

else:
    print("No suitable hedging stocks found.")