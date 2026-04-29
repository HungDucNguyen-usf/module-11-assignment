# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise
            
            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80
    
    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)
        
        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
# 1.1 Create a line chart showing overall quarterly sales trends
# REQUIRED: Function must create and return a matplotlib figure
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    # Your code here
    total_sales = sales_df.groupby("QuarterLabel")["Sales"].sum().reindex(quarter_labels)
    #group by the quarter labels: q1 2022, q2 2023,... then total the sales then map them back to the quarter labels, each quarter a sum
    fig1 = plt.figure(figsize=(8, 5))
    plt.plot(quarter_labels,total_sales, linestyle = "--", marker = "o")
    plt.title("Quarterly sales trend")
    plt.xlabel("Quarter")
    plt.ylabel("Sales ($)")
    plt.grid(True)
    return fig1

# 1.2 Create a multi-line chart comparing sales trends across locations
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig2 = plt.figure(figsize = (8,5))
    for location in locations: #move through each location
        location_sales = sales_df[sales_df["Location"] == location].groupby("QuarterLabel")["Sales"].sum().reindex(quarter_labels)
        #group by the quarter labels, then sum the sales, then map each total sales back to the quarter labels
        plt.plot(quarter_labels,location_sales, linestyle = "--", marker = "o", label = location)
    plt.title("Sales across different locations")
    plt.xlabel("Quarters")
    plt.ylabel("Sales ($)")
    plt.grid(True)
    plt.legend()
    return fig2

# TODO 2: Categorical Comparison - Product Performance by Location
# 2.1 Create a grouped bar chart comparing category performance by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    q4_23 = sales_df[sales_df["QuarterLabel"] == "Q4 2023"] #group them by the latest quarter
    #unstack the pivot table so that we can move the category columns and location index, then calculate the sum of sales
    pivot_table = q4_23.groupby(["Location", "Category"])["Sales"].sum().unstack("Category")
    fig3, ax = plt.subplots(figsize=(8, 5))
    pivot_table.plot(kind = "bar", stacked = False, ax=ax) #this is not a stacked bar chart
    plt.title("Category performance by location")
    plt.ylabel("Total Sales ($)")
    plt.tight_layout()
    return fig3
    
    

# 2.2 Create a stacked bar chart showing the composition of sales in each location
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    # Your code here
    #Similar to the chart above, but this time is the location
    loc_rev = sales_df.groupby(["Location", "Category"])["Sales"].sum().unstack("Category") 
    pivot_percent = loc_rev.div(loc_rev.sum(axis = 1), axis = 0)*100 #calculate the percentage, for each category
    fig4, ax = plt.subplots(figsize=(8, 5))
    pivot_percent.plot(kind = "bar", stacked = True, ax=ax) #this time stack them up
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f%%", label_type="center", fontsize=8) #annotate:
    plt.title("Composition of sales across categories for each location")
    plt.ylabel("Percentages (%)")
    plt.xticks(rotation=45)
    plt.legend(title = "Category",bbox_to_anchor = [1.01, 1], loc = "upper left") #finding a good place to put the legend
    plt.tight_layout()
    return fig4


# TODO 3: Relationship Analysis - Advertising and Sales
# 3.1 Create a scatter plot to examine the relationship between ad spend and sales
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig5 = plt.figure(figsize = (8,5))
    #example from the class lecture, but with the assignment's metrics
    plt.scatter(sales_df["AdSpend"],sales_df["Sales"],alpha=0.7, c=sales_df['AdSpend'], cmap='viridis')
    m,b = np.polyfit(sales_df["AdSpend"], sales_df["Sales"], 1) #make a best fit line formula
    plt.plot(sales_df["AdSpend"], m*sales_df["AdSpend"]+b) #plot the best fir line
    #check if threshold
    threshold = sales_df["Sales"].mean() * 2.5
    threshold2 = sales_df["Sales"].mean() / 2.5
    #outliers
    outliers = sales_df[(threshold <= sales_df["Sales"])|(sales_df["Sales"] <= threshold2)]
    #annotate each outliers
    for _, row in outliers.iterrows():
        plt.annotate(row["Location"], (row["AdSpend"], row["Sales"]), fontsize=8)
    plt.title("Advertising Spend vs. Sales")
    plt.xlabel("Advertising Spend ($)")
    plt.ylabel("Sales ($)")
    return fig5
    

# 3.2 Create a line chart showing sales per dollar spent on advertising over time
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig6 = plt.figure(figsize = (8,5))
    #group by the quarters, then take the mean of the sales per dollar spent, then reindex them
    eff = sales_df.groupby("QuarterLabel")["SalesPerDollarSpent"].mean().reindex(quarter_labels)
    plt.plot(quarter_labels,eff,linestyle = "--",marker = "o")
    plt.title("Ad efficiency over time")
    plt.xlabel("Quarter")
    plt.ylabel("Sales per Ad Dollar ($)")
    #which quarter? What is the value?
    best_quarter = eff.idxmax()
    best_value = eff.max()
    #annotate
    plt.annotate(f"Best: {best_quarter} at ${best_value:.2f}", (best_quarter, best_value), textcoords="offset points", xytext=(10, -15), fontsize=8, color="red")
    plt.grid(True)
    return fig6

# TODO 4: Distribution Analysis - Customer Demographics
# 4.1 Create histograms of customer age distribution
# REQUIRED: Function must create and return a matplotlib figure with subplots
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig7, axes = plt.subplots(2,3,figsize = (12,6))
    #flatten to convert 2D grid (2 rows 3 columns) into a simple list [axes[0], axes[1], ...]
    axes = axes.flatten()
    #make a histogram based on age, with each group is 15 years apart
    axes[0].hist(customer_df["Age"], bins = 15, edgecolor = "black")
    #mark the mean and median age of all locations
    axes[0].axvline(customer_df["Age"].mean(), color="red", linestyle="-", label=f"Mean: {customer_df['Age'].mean():.1f}")
    axes[0].axvline(customer_df["Age"].median(), color="yellow", linestyle="-", label=f"Median: {customer_df['Age'].median():.1f}")
    axes[0].set_title("All Locations")
    axes[0].set_xlabel("Age")
    axes[0].set_ylabel("Amount of people")
    axes[0].legend()
    for i, loc in enumerate(locations, start = 1): #index each location, since each subplot is one location
        #similar to the above, just now group by location instead
        age = customer_df[customer_df["Location"] == loc]["Age"]
        axes[i].hist(age, bins = 15, edgecolor = "black") 
        axes[i].axvline(age.mean(), color="red", linestyle="-", label=f"Mean: {age.mean():.1f}")
        axes[i].axvline(age.median(), color="yellow", linestyle="-", label=f"Median: {age.median():.1f}")
        axes[i].set_title(f"{loc}")
        axes[i].set_xlabel("Age")
        axes[i].set_ylabel("Amount of people")
        axes[i].legend()
    axes[5].set_visible(False)
    plt.tight_layout()
    return fig7
# 4.2 Create box plots comparing purchase amounts by age groups
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig8 = plt.figure(figsize = (8,5))
    #pd.cut() to get the age groups
    customer_df["AgeGroup"] = pd.cut(customer_df["Age"], bins = [18,30,45,60,100], labels = ["18-30","31-45","46-60","61+"])
    #label each age group
    age_group = ["18-30","31-45","46-60","61+"]
    #list comprehension for the boxplot
    groups = [customer_df[customer_df["AgeGroup"] == ag]["PurchaseAmount"].values for ag in age_group]
    plt.boxplot(groups, tick_labels = age_group)
    plt.title("Purchase amounts by age groups")
    plt.xlabel("Age groups")
    plt.ylabel("Purchase amount ($)")
    plt.grid(True)
    return fig8
# TODO 5: Sales Distribution - Pricing Tiers
# 5.1 Create a histogram of purchase amounts
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig9 = plt.figure(figsize = (8,5))
    #basic purchase amount
    plt.hist(customer_df["PurchaseAmount"],bins = 25, edgecolor = "black")
    plt.title("Purchase amounts")
    plt.xlabel("Purchase amounts")
    plt.ylabel("Amount of people")
    return fig9

# 5.2 Create a pie chart showing sales breakdown by price tier
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig10 = plt.figure(figsize = (8,5))
    #group by the price tier, then total the sales, then map them back
    purchase_by_tier = customer_df.groupby("PriceTier")["PurchaseAmount"].sum().reindex(["Budget","Mid-range","Premium"])
    #label the pie chart, put percentages, then explode the biggest one
    plt.pie(purchase_by_tier, labels = ["Budget", "Mid-range", "Premium"], autopct = "%1.1f%%", explode = (0,0.05,0))
    plt.title("Purchase amount by price tier")
    return fig10
# TODO 6: Market Share Analysis
# 6.1 Create a pie chart showing sales breakdown by category
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig11 = plt.figure(figsize = (8,5))
    #similar to above, but now the category sales
    sales_by_cat = sales_df.groupby("Category")["Sales"].sum().reindex(categories)
    plt.pie(sales_by_cat, labels = categories, autopct = "%1.1f%%", explode = (0.05,0,0,0,0))
    plt.title("Sales by categories")
    return fig11
# 6.2 Create a pie chart showing sales breakdown by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig12 = plt.figure(figsize = (8,5))
    #similar to above, but now location sales
    sales_by_loc = sales_df.groupby("Location")["Sales"].sum().reindex(locations)
    plt.pie(sales_by_loc, labels = locations, autopct = "%1.1f%%", explode = (0,0.05,0,0))
    plt.title("Sales by locations")
    return fig12
# TODO 7: Comprehensive Dashboard
# REQUIRED: Function must create and return a matplotlib figure with at least 4 subplots
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    # Your code here
    fig13, axes = plt.subplots(2,2,figsize = (15,10))
    axes = axes.flatten()
    fig13.suptitle("SunCoast Retail Business Dashboard", fontsize=16, fontweight="bold")
    #copy the figure 2 then change from 1 plot to 1 subplot
    for location in locations: #move through each location
        location_sales = sales_df[sales_df["Location"] == location].groupby("QuarterLabel")["Sales"].sum().reindex(quarter_labels)
        #group by the quarter labels, then sum the sales, then map each total sales back to the quarter labels
        axes[0].plot(quarter_labels,location_sales, linestyle = "--", marker = "o", label = location)
    axes[0].set_title("Sales across different locations")
    axes[0].set_xlabel("Quarters")
    axes[0].set_ylabel("Sales ($)")
    axes[0].grid(True)
    axes[0].legend()
    #copy figure 3
    q4_23 = sales_df[sales_df["QuarterLabel"] == "Q4 2023"]
    pivot_table = q4_23.groupby(["Location", "Category"])["Sales"].sum().unstack("Category")
    pivot_table.plot(kind = "bar", stacked = False, ax=axes[1])
    axes[1].set_title("Category performance by location")
    axes[1].set_ylabel("Total Sales ($)")
    #copy figure 9 
    axes[2].hist(customer_df["PurchaseAmount"],bins = 25, edgecolor = "black")
    axes[2].set_title("Purchase amounts")
    axes[2].set_xlabel("Purchase amounts")
    axes[2].set_ylabel("Amount of people")
    #copy fig 10
    purchase_by_tier = customer_df.groupby("PriceTier")["PurchaseAmount"].sum().reindex(["Budget","Mid-range","Premium"])
    axes[3].pie(purchase_by_tier, labels = ["Budget", "Mid-range", "Premium"], autopct = "%1.1f%%", explode = (0,0.05,0))
    axes[3].set_title("Purchase amount by price tier")
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)
    return fig13
# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)
    
    # REQUIRED: Call all visualization functions and store figures
    # Store each figure in a variable for potential saving/display
    
    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    
    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    
    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    
    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    
    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    
    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    
    # Comprehensive Dashboard
    fig13 = create_business_dashboard()
    
    # REQUIRED: Add business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    # Your insights here based on the visualizations
    print("1/Tampa is the location with the highest sales last quarter")
    print("2/Electronic is the best selling category")
    print("3/People buy mid-range price tier the most")
    print("4/The purchase amount that people usually do is around 80")
    print("5/The ad efficiency took a dip in Q1 2023, but has risen up again in the latest quarter")
    # Display all figures
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()