import datadotworld as dw
import pandas as pd
import numpy as np

#import data using dataworld API
acquisitions_df = dw.query(
    'lynxrose/startup-analysis',
    '''SELECT company_name,
    acquired_at, price_amount
    FROM acquisitions WHERE company_country_code = 'USA' and price_currency_code = 'USD'
    ''').dataframe

company_df = dw.query(
    'lynxrose/startup-analysis',
    '''SELECT name, market, funding_total_usd, status, funding_rounds,
    State_code, City,founded_at
    FROM companies WHERE country_code = 'USA'
    ''').dataframe

#Merging the data
full_df = pd.merge(company_df,acquisitions_df, how='left', left_on=['name'], right_on=['company_name'])

#Creating managable categories (category names are on index 0)
medical = ['Medical','Pharmaceuticals','Biotechnology','Health Care','Health and Wellness','Bio-Pharm','Medical Devices','Health Care Information Technology','Genetic Testing','Electronic Health Records','Bioinformatics','Healthcare Services','Hospitals','Physicians','Therapeutics','Clinical Trials','Health and Insurance','Dental','Medical Professionals','Diagnostics','Diabetes','Psychology','Medical Marijuana Patients','Doctors','Senior Health','Elder Care','mHealth','Synthetic Biology','Biometrics']

manufacuring = ['Manufacturing','Automotive', 'Cars', 'Embedded Hardware and Software','Semiconductors','Sensors','Communications Hardware','Residential Solar','Mobile Devices','Clean Energy','Environmental Innovation','Heavy Industry','Industrial Automation','Nanotechnology','Computers','Commercial Solar','Biotechnology and Semiconductor','Industrial','Semiconductor Manufacturing Equipment','Boating Industry','Wind','Solar']

federal_contracting = ['Federal_Contracting','Law Enforcement','Governments','Ticketing','DOD/Military','Governance','Government Innovation']

renting = ['Renting','Data Centers','Realtors','Vacation Rentals','Music Venues','Self Storage','Office Space','Timeshares','Parking','Rental Housing','Real Estate','Commercial Real Estate','Outdoor Advertising']

fitness = ['Fitness','Sports','Training','Self Development','Nutrition','Exercise','Personal Health','Lifestyle']

science_and_engineering = ['Science_and_Engineering','Aerospace','Space Travel','Robotics','Life Sciences','Neuroscience','Material Science','Renewable Energies','Energy','Humanitarian','Engineering Firms','Energy Management','Energy Efficiency','Green','Energy IT','Water Purification','Industrial Energy Efficiency','Renewable Tech','Natural Resources','Sustainability','Mechanical Solutions']

transportation = ['Transportation','Distribution','Public Transportation','Shipping','Postal and Courier Services','Distributors','Recycling']

banking = ['Banking','Credit','Credit Cards','Venture Capital','Financial Services','Accounting','Insurance','Retirement','Brokers','Home Owners','Angels','Real Estate Investors','Hedge Funds']

labor = ['Labor','Agriculture','Construction','Home & Garden','Home Renovation','Food Processing','Architecture','Farming']

gaming = ['Gaming','Games','Entertainment','Video Games','Gambling','Fantasy Sports','Educational Games','Online Gaming','MMO Games','PC Gaming','Game','Entertainment Industry','Game Mechanics','FreetoPlay Gaming','Digital Entertainment']

art = ['Art','Design','Fashion','Photography','Art','Indoor Positioning','Music Services','Audio','Graphics','Film','Product Design','Content Creators','Interior Design','Lighting','Writers','Creative Industries','Designers','Recipes','Music','Creative','Film Production','News','Publishing','Journalism']

service = ['Service','Hospitality','Travel','Customer Service','Hotels','Weddings','Funeral Industry','Pets','Leisure','Concerts','Adventure Travel','Tourism','Social Travel','Taxis','Travel & Tourism','Service Industries','Nightclubs','Senior Citizens','Cosmetic Surgery','Plumbers','Cooking','Restaurants','Personal Finance']

corporate_services = ['Corporate_Services','Property Management','Digital Rights Management','Legal','Services','Personal Branding','Business Services','Logistics','Consulting','Investment Management','Wealth Management','Supply Chain Management','CRM','Intellectual Asset Management','Recruiting','Unifed Communications','Loyalty Programs','Promotional','Reputation','Market Research','Price Comparison','Project Management','Human Resources','Infrastructure','Product Development Services','Innovation Management','Corporate Wellness','Professional Services','Monetization','Incentives','Logistics Company','Career Planning','Content Delivery','Corporate IT','Enterprise Resource Planning','Collaborative Consumption','Contact Management','Performance Marketing','Opinions','Corporate Training','Business Productivity','Risk Management', 'Licensing','Lead Generation','Offline Businesses','Business Development','Lead Management','Bridging Online and Offline','Employer Benefits Programs','Classifieds','IT Management','Direct Marketing','Advertising Exchanges','Sponsorship','Knowledge Management','Staffing Firms','Fleet Management','Estimation and Quoting','Franchises','Procurement','Translation','Polling','Brand Marketing','Quantitative Marketing','Billing','Career Management','Public Relations','Freelancers']

remove_list = ['Other','Local Businesses','Small and Medium Businesses','Local','Startups','Enterprises','Location Based Services','Communities','Consumers','Synchronization','Advice','Outdoors','Radical Breakthrough Startups','Rapidly Expanding','All Markets','Employment','Lifestyle Businesses','DIY','World Domination','Q&A','Contests','Baby Boomers','Multi-level Marketing','Emerging Markets','Moneymaking','Women','Real Time','Ediscovery','Freemium','Enterprise 2.0','Advanced Materials','Politics','nan','Celebrity','Coworking','Entrepreneur']

retail = ['Retail','Shoes','Consumer Electronics','Auctions','Oil & Gas','Oil and Gas','Displays','Sporting Goods','Cosmetics', 'Electronics','Drones','Consumer Goods','Gift Card','Wine And Spirits','Water','Organic','Utilities','Home Automation','Home Decor','Green Consumer Goods','Beauty','Batteries','Animal Feed','Groceries','Commodities','Golf Equipment','Organic Food','Specialty Foods','Craft Beer','Oil','Specialty Chemicals','Chemicals','Textiles','Tablets','Gas','Bicycles','Farmers Market','Auto','Auto','Toys', 'Tea','Jewelry','Specialty Retail','Textbooks','Dietary Supplements','Twin-Tip Skis','Lifestyle Products','Sunglasses','Baby Accessories','Electric Vehicles','Coffee','Spas']

education = ['Education','Colleges','Teachers','Kids','Tutoring','K-12 Education','High Schools','Technical Continuing Education','All Students','Guides','Skill Assessment','Incubators','Charter Schools','College Recruiting','Alumni','Certification Test','Defense','Language Learning','Testing','English-Speaking','Universities','Registrars','Test and Measurement','Babies','College Campuses','Religion', 'Parenting','Families']

nonprofit = ['Nonprofits','Non Profit','Charity']

market_list = [education,nonprofit,retail,remove_list,corporate_services,service, art, gaming, labor, banking, transportation, science_and_engineering,fitness, renting, federal_contracting, manufacuring, medical]

#function which returns the category, unmarked categories where Online_Tech
def market_simplifier(string):
    found = False
    for market in market_list:
        if string in market:
            found = True
            return market[0]
    if found == False:
        return 'Online_Tech'

#map the function above
full_df['market'] = full_df['market'].apply(market_simplifier)

#remove None and NaNs
full_df.mask(full_df.eq('None')).dropna()

#export the data
full_df.to_csv('cleaned.csv')