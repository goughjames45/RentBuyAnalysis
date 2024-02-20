import numpy as np
import matplotlib.pyplot as plt

# Define parameters and distributions
num_simulations = 10000
home_value = 450000  # Initial home value
home_appreciation = 0.035
home_appreciation_std = 0.01
down_payment_percent = 0.2
down_payment = home_value * down_payment_percent
loan_amount = home_value - down_payment
mortgage_rate = 0.07
mortgage_term_years = 30
property_tax_rate = 0.012
home_insurance_annual = 1000
maintenance_percent = 0.01
hoa_fee = 300
rent_initial = 2800
rent_increase_mean = 0.03
rent_increase_std = 0.01
parking_fee = 275
stock_market_return_mean = 0.1
stock_market_return_std = 0.05

# Generate random samples
home_price_appreciation_samples = np.random.normal(home_appreciation, home_appreciation_std, num_simulations)
rent_increase_samples = np.random.normal(rent_increase_mean, rent_increase_std, num_simulations)
stock_market_return_samples = np.random.normal(stock_market_return_mean, stock_market_return_std, num_simulations)

# Calculate monthly costs and savings for each simulation
monthly_costs_owning = []
monthly_costs_renting = []

for i in range(num_simulations):
    monthly_interest_rate = mortgage_rate / 12
    num_payments = mortgage_term_years * 12
    mortgage_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**num_payments) / ((1 + monthly_interest_rate)**num_payments-1) 
    property_taxes = home_value * property_tax_rate / 12
    home_insurance_monthly = home_insurance_annual / 12
    future_value = home_value * (1 + home_price_appreciation_samples[i])**10
    maintenance_monthly_start = home_value * maintenance_percent / 12
    maintenance_monthly_future = future_value * maintenance_percent / 12

    maintenance_monthly = (maintenance_monthly_start + maintenance_monthly_future) / 2
    future_value = home_value * (1 + home_price_appreciation_samples[i])**10
    avg_monthly_appreciation = (future_value - home_value) / (12*10)
    total_monthly_cost_owning = mortgage_payment + property_taxes + home_insurance_monthly + maintenance_monthly + hoa_fee - avg_monthly_appreciation
    monthly_costs_owning.append(total_monthly_cost_owning)

    rent_current = rent_initial
    total_monthly_cost_renting = rent_current + parking_fee
    monthly_costs_renting.append(total_monthly_cost_renting)

# Calculate opportunity cost of down payment in stock market
opportunity_cost_samples = down_payment * (stock_market_return_samples / 12)

# Adjust net monthly savings for owning vs renting by opportunity cost
net_monthly_savings = np.subtract(monthly_costs_renting, monthly_costs_owning)
net_monthly_savings_adjusted = np.subtract(net_monthly_savings, opportunity_cost_samples)

# Calculate summary statistics
mean_savings = np.mean(net_monthly_savings_adjusted)
median_savings = np.median(net_monthly_savings_adjusted)
std_dev_savings = np.std(net_monthly_savings_adjusted)
percent_positive_savings = np.sum(net_monthly_savings_adjusted > 0) / num_simulations

# Visualize distribution of net monthly savings
plt.hist(net_monthly_savings_adjusted, bins=50, density=True, alpha=0.7, color='blue')
plt.xlabel('Net Monthly Savings (Renting vs. Owning)')
plt.ylabel('Density')
plt.title('Distribution of Net Monthly Savings (Renting vs. Owning)')
plt.axvline(x=0, color='red', linestyle='--', linewidth=1)
plt.text(0.05, 0.95, f'Mean: ${mean_savings:.2f}\nMedian: ${median_savings:.2f}\nStd Dev: ${std_dev_savings:.2f}\nPercent Positive: {percent_positive_savings:.2%}', transform=plt.gca().transAxes)
plt.grid(True)
plt.show()

