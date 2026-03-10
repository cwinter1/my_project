# ══════════════════════════════════════════════════════════════
#  WEEK 3  |  DAY 5  |  WEB SCRAPING
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand web scraping concepts and set up requests + BeautifulSoup
#  2. Find and extract HTML elements using find(), find_all(), and CSS selectors
#  3. Extract HTML tables into pandas DataFrames using pd.read_html()
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python BeautifulSoup web scraping tutorial"
#  Search: "Python pandas read_html table scraping"
# ══════════════════════════════════════════════════════════════

# All examples in this lesson use inline HTML strings, not live URLs.
# This makes the code run reliably without a network connection.
#
# Install if needed:
#   pip install beautifulsoup4
#   pip install lxml        (faster HTML parser, optional but recommended)

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS WEB SCRAPING, requests + BeautifulSoup SETUP
# ══════════════════════════════════════════════════════════════
# Web scraping is the process of extracting data from HTML web pages.
# The typical workflow:
#   1. Fetch the HTML of a page using requests.get()
#   2. Parse the HTML into a tree structure using BeautifulSoup
#   3. Navigate and search the tree to extract the data you need
#
# BeautifulSoup understands the nested structure of HTML (tags, attributes, text).
# You tell it WHAT to look for and it returns the matching elements.
#
# IMPORTANT NOTES:
#   - Always check a website's robots.txt and Terms of Service before scraping
#   - Be respectful: add time.sleep() delays between requests
#   - Many sites prefer you use their official API instead of scraping

# EXAMPLE ──────────────────────────────────────────────────────
try:
    from bs4 import BeautifulSoup

    # A simple HTML page for a company's employee directory
    html_employee_directory = """
    <html>
    <head><title>Employee Directory</title></head>
    <body>
        <h1 id="page-title">TechCorp Employee Directory</h1>
        <p class="subtitle">Q4 2024 — Active Employees Only</p>
        <div class="department" id="dept-engineering">
            <h2>Engineering</h2>
            <ul class="employee-list">
                <li class="employee"><span class="name">Alice Ng</span> — <span class="role">Senior Engineer</span></li>
                <li class="employee"><span class="name">Dave Park</span> — <span class="role">Lead Engineer</span></li>
            </ul>
        </div>
        <div class="department" id="dept-sales">
            <h2>Sales</h2>
            <ul class="employee-list">
                <li class="employee"><span class="name">Bob Chen</span> — <span class="role">Account Executive</span></li>
                <li class="employee"><span class="name">Eve Torres</span> — <span class="role">Sales Manager</span></li>
            </ul>
        </div>
    </body>
    </html>
    """

    # Parse the HTML — "html.parser" is the built-in Python parser
    # Use "lxml" instead if you have it installed (faster and more tolerant)
    soup = BeautifulSoup(html_employee_directory, "html.parser")

    # Navigate to specific tags
    title_tag = soup.find("h1")
    print("Page title:", title_tag.text)
    # TechCorp Employee Directory

    # Access tag attributes
    title_id = title_tag.get("id")
    print("Title element ID:", title_id)
    # page-title

    # Find a tag by ID attribute
    eng_div = soup.find("div", id="dept-engineering")
    print("Engineering section heading:", eng_div.find("h2").text)
    # Engineering

    # Get all department headings
    headings = soup.find_all("h2")
    print("Departments:", [h.text for h in headings])
    # ['Engineering', 'Sales']

    # Prettify shows the formatted HTML structure
    print("\nParsed structure preview:")
    print(soup.find("p", class_="subtitle").prettify())

except ImportError:
    print("BeautifulSoup not installed. Run: pip install beautifulsoup4")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Parse the HTML below and extract product information.
#
# Tasks:
#   1. Find the page heading (<h1>) and print it
#   2. Find all <div class="product"> elements
#   3. For each product, extract and print: name, price, and availability
#
# Expected output:
#   Page: Product Catalog -- Fall 2024
#   Widget A    | $19.99  | In Stock
#   Widget B    | $34.99  | Out of Stock
#   Gadget X    | $89.99  | In Stock
#   Gadget Y    | $129.99 | In Stock

html_catalog = """
<html>
<body>
    <h1>Product Catalog -- Fall 2024</h1>
    <div class="product" data-sku="SKU-001">
        <span class="product-name">Widget A</span>
        <span class="price">$19.99</span>
        <span class="availability">In Stock</span>
    </div>
    <div class="product" data-sku="SKU-002">
        <span class="product-name">Widget B</span>
        <span class="price">$34.99</span>
        <span class="availability">Out of Stock</span>
    </div>
    <div class="product" data-sku="SKU-003">
        <span class="product-name">Gadget X</span>
        <span class="price">$89.99</span>
        <span class="availability">In Stock</span>
    </div>
    <div class="product" data-sku="SKU-004">
        <span class="product-name">Gadget Y</span>
        <span class="price">$129.99</span>
        <span class="availability">In Stock</span>
    </div>
</body>
</html>
"""




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — FINDING ELEMENTS: find(), find_all(), CSS SELECTORS
# ══════════════════════════════════════════════════════════════
# find(tag)                     -- returns the FIRST matching element (or None)
# find_all(tag)                 -- returns a LIST of all matching elements
# find(tag, class_="name")      -- find by tag AND class (class_ because class is reserved)
# find(tag, id="my-id")         -- find by tag AND id
# find_all(tag, attrs={})       -- find by arbitrary attributes
# select("css selector")        -- use CSS selector syntax (very powerful)
# select_one("css selector")    -- CSS selector returning first match only
#
# CSS selector examples:
#   "div"                  -- all div elements
#   ".product"             -- elements with class "product"
#   "#main-table"          -- element with id "main-table"
#   "table tr"             -- all tr inside a table
#   "span.price"           -- span with class "price"
#   "a[href]"              -- links that have an href attribute
#   "tr:nth-of-type(2)"    -- second tr element

# EXAMPLE ──────────────────────────────────────────────────────
try:
    from bs4 import BeautifulSoup

    html_sales_report = """
    <html>
    <body>
        <div id="report-header">
            <h2>Sales Report Q3 2024</h2>
            <p class="generated-by">Generated by: BI System</p>
        </div>
        <table id="sales-data" class="data-table">
            <thead>
                <tr>
                    <th>Region</th>
                    <th>Rep</th>
                    <th>Revenue</th>
                    <th>Deals</th>
                </tr>
            </thead>
            <tbody>
                <tr class="data-row">
                    <td class="region">West</td>
                    <td class="rep">Tom Reyes</td>
                    <td class="revenue" data-value="185000">$185,000</td>
                    <td class="deals">12</td>
                </tr>
                <tr class="data-row">
                    <td class="region">East</td>
                    <td class="rep">Priya Mehta</td>
                    <td class="revenue" data-value="312000">$312,000</td>
                    <td class="deals">18</td>
                </tr>
                <tr class="data-row">
                    <td class="region">Central</td>
                    <td class="rep">Sara Jones</td>
                    <td class="revenue" data-value="154000">$154,000</td>
                    <td class="deals">11</td>
                </tr>
            </tbody>
        </table>
        <div class="footnotes">
            <a href="/report/details">View full details</a>
            <a href="/export/csv">Download CSV</a>
        </div>
    </body>
    </html>
    """

    soup = BeautifulSoup(html_sales_report, "html.parser")

    # find() — single element
    header = soup.find("div", id="report-header")
    print(header.find("h2").text)                    # Sales Report Q3 2024

    # find_all() — multiple elements
    rows = soup.find_all("tr", class_="data-row")
    print(f"Data rows: {len(rows)}")                 # 3

    # Extract data from each row
    print("\nRep performance:")
    for row in rows:
        region = row.find("td", class_="region").text
        rep = row.find("td", class_="rep").text
        revenue = row.find("td", class_="revenue")
        # Get the raw numeric value from a data attribute (easier than parsing "$185,000")
        raw_value = int(revenue.get("data-value"))
        print(f"  {region:<10} | {rep:<15} | ${raw_value:>10,}")

    # CSS selectors — more flexible
    all_reps = [td.text for td in soup.select("td.rep")]
    print("\nAll reps:", all_reps)                   # ['Tom Reyes', 'Priya Mehta', 'Sara Jones']

    # Get all links and their href attributes
    links = soup.select("a[href]")
    for link in links:
        print(f"  Link: {link.text:<20} -> {link['href']}")

    # Find elements containing specific text
    high_rev = soup.find("td", string="$312,000")
    if high_rev:
        parent_row = high_rev.find_parent("tr")
        top_rep = parent_row.find("td", class_="rep").text
        print(f"\nTop performer: {top_rep}")          # Priya Mehta

except ImportError:
    print("BeautifulSoup not installed.")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Parse the HTML below representing a job board.
# Extract all job listings and build a list of dicts.
#
# For each listing extract: title, department, location, salary
# (salary is stored in the data-salary attribute as a number)
#
# Then:
#   1. Print all listings
#   2. Print only listings where salary > 80000
#   3. Print the average salary across all listings
#
# Expected output:
#   Data Engineer      | Engineering | Remote    | $95,000
#   Sales Analyst      | Sales       | New York  | $72,000
#   BI Developer       | Engineering | Chicago   | $88,000
#   Finance Manager    | Finance     | Boston    | $105,000
#   SDR                | Sales       | Remote    | $65,000
#
#   High-value roles (>$80k):
#   Data Engineer, BI Developer, Finance Manager
#
#   Average salary: $85,000.00

html_jobs = """
<html>
<body>
    <h1>Open Positions</h1>
    <div class="job-listing" data-salary="95000">
        <span class="job-title">Data Engineer</span>
        <span class="department">Engineering</span>
        <span class="location">Remote</span>
    </div>
    <div class="job-listing" data-salary="72000">
        <span class="job-title">Sales Analyst</span>
        <span class="department">Sales</span>
        <span class="location">New York</span>
    </div>
    <div class="job-listing" data-salary="88000">
        <span class="job-title">BI Developer</span>
        <span class="department">Engineering</span>
        <span class="location">Chicago</span>
    </div>
    <div class="job-listing" data-salary="105000">
        <span class="job-title">Finance Manager</span>
        <span class="department">Finance</span>
        <span class="location">Boston</span>
    </div>
    <div class="job-listing" data-salary="65000">
        <span class="job-title">SDR</span>
        <span class="department">Sales</span>
        <span class="location">Remote</span>
    </div>
</body>
</html>
"""




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — EXTRACTING TABLES WITH pandas read_html()
# ══════════════════════════════════════════════════════════════
# pd.read_html() finds ALL <table> elements in an HTML string or URL
# and returns them as a list of DataFrames.
#
# This is by far the fastest way to extract structured table data from HTML.
# No need to loop through rows and cells manually.
#
# Syntax:
#   tables = pd.read_html(html_string)   -- returns a list of DataFrames
#   tables = pd.read_html(html_string, match="Revenue")  -- only tables containing "Revenue"
#   tables[0]  -- first table found
#
# Requires: pip install lxml   (or html5lib as fallback)

# EXAMPLE ──────────────────────────────────────────────────────
try:
    import pandas as pd

    html_with_tables = """
    <html>
    <body>
        <h2>Monthly Sales Summary</h2>
        <table id="monthly-sales" border="1">
            <tr><th>Month</th><th>Region</th><th>Revenue</th><th>Units</th></tr>
            <tr><td>January</td><td>West</td><td>142000</td><td>284</td></tr>
            <tr><td>January</td><td>East</td><td>198000</td><td>396</td></tr>
            <tr><td>February</td><td>West</td><td>155000</td><td>310</td></tr>
            <tr><td>February</td><td>East</td><td>211000</td><td>422</td></tr>
            <tr><td>March</td><td>West</td><td>169000</td><td>338</td></tr>
            <tr><td>March</td><td>East</td><td>225000</td><td>450</td></tr>
        </table>

        <h2>Expense Summary</h2>
        <table id="expenses" border="1">
            <tr><th>Category</th><th>Budget</th><th>Actual</th><th>Variance</th></tr>
            <tr><td>Marketing</td><td>50000</td><td>47500</td><td>2500</td></tr>
            <tr><td>Operations</td><td>120000</td><td>131000</td><td>-11000</td></tr>
            <tr><td>R&amp;D</td><td>200000</td><td>189000</td><td>11000</td></tr>
        </table>
    </body>
    </html>
    """

    # Read all tables — returns a list
    tables = pd.read_html(html_with_tables)
    print(f"\nNumber of tables found: {len(tables)}")   # 2

    # First table: monthly sales
    df_sales = tables[0]
    print("\nMonthly Sales Table:")
    print(df_sales)
    print("\nTotal revenue:", df_sales["Revenue"].sum())   # 1100000
    print("Revenue by region:")
    print(df_sales.groupby("Region")["Revenue"].sum())

    # Second table: expenses
    df_expenses = tables[1]
    print("\nExpense Table:")
    print(df_expenses)
    print("\nOver-budget categories:")
    over_budget = df_expenses[df_expenses["Variance"] < 0]
    print(over_budget[["Category", "Variance"]])

    # Save to CSV for later analysis
    import os
    this_dir = os.path.dirname(__file__)
    df_sales.to_csv(os.path.join(this_dir, "scraped_sales.csv"), index=False)
    print("\nSaved scraped_sales.csv")

except ImportError as e:
    print(f"Required package not installed: {e}")
    print("Run: pip install pandas lxml")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Use pd.read_html() to extract the leaderboard table below.
# Then perform analysis using pandas:
#   1. Load the table into a DataFrame
#   2. Find the rep with the highest "Deals Closed"
#   3. Calculate total revenue for each department
#   4. Find all reps where "Quota Attainment %" >= 100
#
# Expected output:
#   Top closer: Priya Mehta (18 deals)
#   Revenue by department:
#   Sales    891000
#   Reps at 100% quota or above:
#   Priya Mehta | 104.0%
#   Sara Jones  | 102.7%

html_leaderboard = """
<html>
<body>
<table>
    <tr>
        <th>Rep Name</th>
        <th>Department</th>
        <th>Deals Closed</th>
        <th>Revenue</th>
        <th>Quota Attainment %</th>
    </tr>
    <tr><td>Tom Reyes</td><td>Sales</td><td>12</td><td>185000</td><td>92.5</td></tr>
    <tr><td>Priya Mehta</td><td>Sales</td><td>18</td><td>312000</td><td>104.0</td></tr>
    <tr><td>Sara Jones</td><td>Sales</td><td>11</td><td>154000</td><td>102.7</td></tr>
    <tr><td>Omar Nasser</td><td>Sales</td><td>7</td><td>98000</td><td>65.3</td></tr>
    <tr><td>Lena Kim</td><td>Sales</td><td>9</td><td>142000</td><td>85.1</td></tr>
</table>
</body>
</html>
"""


