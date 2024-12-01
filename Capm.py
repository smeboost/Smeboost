import streamlit as st
from openai import OpenAI
import datetime
import re
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, NextPageTemplate
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import datetime
import re
import os
import uuid
from reportlab.platypus import Frame, PageTemplate, BaseDocTemplate, PageBreak
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, NextPageTemplate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# Constants
BUSINESS_OPTIONS = {
    "Business Valuation": "I want to assess my company's worth, helping me make informed decisions and gain investor trust.",
    "Financial Healthcheck": "I want to review my finances, checking assets, debts, cash flow, and overall stability",
    "Business Partnering": "I want to build partnerships to grow, sharing strengths and resources with others for mutual benefit.",
    "Fund Raising": "I want to secure funds from investors to expand, innovate, or support my business operations.",
    "Bankability and Leverage": "I want to evaluate my creditworthiness, improving access to financing and managing debt effectively.",
    "Mergers and Acquisitions": "I want to pursue growth by combining my business with others, expanding resources and market reach.",
    "Budget and Resourcing": "I want to allocate resources wisely to achieve my goals efficiently and boost productivity.",
    "Business Remodelling": "I want to reshape my operations to stay relevant and seize new market opportunities.",
    "Succession Planning": "I want to prepare for future leadership transitions, ensuring the right people continue my business legacy."
}

# Utility Functions
def get_openai_response(prompt, system_content, api_key):
    """
    Function to interact with OpenAI API.
    """
    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error communicating with OpenAI API: {str(e)}")
        return None

def initialize_session_state():
    """
    Initialize the session state variables
    """
    if 'show_options' not in st.session_state:
        st.session_state.show_options = False
    if 'show_profile' not in st.session_state:
        st.session_state.show_profile = False
    if 'show_business_priority' not in st.session_state:
        st.session_state.show_business_priority = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
def render_personal_profile_form():
    """Render the personal profile form at the start of the application"""
    with st.form(key="personal_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name*", key="full_name")
            email = st.text_input("Email Address*", key="email")
        
        with col2:
            phone = st.text_input("Mobile Number*", key="phone")
        
        # Additional company information
        if 'business_profile' in st.session_state:
            company_name = st.session_state['business_profile'].get('company_name', '')
        else:
            company_name = ''

        submit = st.form_submit_button("Submit Personal Profile")
        if submit:
            # Validate required fields
            if not all([full_name, email, phone]):
                st.error("Please fill in all required fields marked with *")
                return None
            
            # Validate email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address")
                return None
            
            # Store in session state and return
            profile_data = {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "company_name": company_name,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return profile_data
    return None
def render_header():
    """Render application header"""
    col1, col2 = st.columns([3, 1])
    with col1:
        logo_path = "smeimge.jpg"
        if os.path.exists(logo_path):
            st.image(logo_path, width=100)
    with col2:
        logo_path = "finb.jpg"
        if os.path.exists(logo_path):
            st.image(logo_path, width=100)

# Form Rendering Functions
def render_business_profile_form():
    st.write("### Business Profile")
    with st.form(key="business_profile_form"):
        company_name = st.text_input("Company Name")
        
        business_model = st.text_area(
            "Describe how your company makes money (max 150 words)",
            max_chars=150
        )
        
        products_services = st.text_area(
            "Describe your products/services (max 150 words)",
            max_chars=150
        )
        
        industry = st.selectbox(
            "Select your industry",
            options=[
                "Accommodation and Food Service Activities",
                "Administrative and Support Service Activities",
                "Agriculture, Forestry, and Fishing",
                "Arts, Entertainment, and Recreation",
                "Construction",
                "Education",
                "Electricity, Gas, Steam, and Air Conditioning Supply",
                "Financial and Insurance/Takaful Activities",
                "Human Health and Social Work Activities",
                "Information and Communication",
                "Manufacturing",
                "Mining and Quarrying",
                "Professional, Scientific, and Technical Activities",
                "Public Administration and Defence; Compulsory Social Security",
                "Real Estate Activities",
                "Transportation and Storage",
                "Water Supply, Sewerage, Waste Management, and Remediation Activities",
                "Wholesale and Retail Trade; Repair of Motor Vehicles and Motorcycles",
                "Others please specify"
            ]
        )
        
        other_industry_details = None
        if industry == "Others please specify":
            other_industry_details = st.text_input("Please specify your industry")

        incorporation_status = st.radio(
            "Is your company incorporated in Malaysia with primary business operations based locally?",
            ["Yes", "No", "Others"]
        )
        
        other_incorporation_details = None
        if incorporation_status == "Others":
            other_incorporation_details = st.text_input("Please specify your incorporation status")

        primary_currency = st.selectbox(
            "Select your primary currency",
            options=[
                "Malaysian Ringgit (MYR)",
                "United States Dollar (USD)",
                "Euro (EUR)",
                "British Pound Sterling (GBP)",
                "Japanese Yen (JPY)",
                "Australian Dollar (AUD)",
                "Canadian Dollar (CAD)",
                "Swiss Franc (CHF)",
                "Chinese Yuan (CNY)",
                "Singapore Dollar (SGD)",
                "Indian Rupee (INR)",
                "New Zealand Dollar (NZD)",
                "South Korean Won (KRW)",
                "Hong Kong Dollar (HKD)",
                "Thai Baht (THB)",
                "Philippine Peso (PHP)",
                "Indonesian Rupiah (IDR)",
                "Vietnamese Dong (VND)",
                "Saudi Riyal (SAR)",
                "Emirati Dirham (AED)",
                "Turkish Lira (TRY)",
                "Brazilian Real (BRL)",
                "South African Rand (ZAR)",
                "Mexican Peso (MXN)",
                "Russian Ruble (RUB)"
            ]
        )

        revenue_size = st.radio(
            "My annual revenue size is between (choose one)",
            ["<1m", "1 - 5m", "5 - 10m", ">10 - 30m", ">30 - 50m", ">50m"]
        )

        profit_range = st.radio(
            "Company's profit range? (choose one)",
            ["<100k", "100 - 500k", ">500k - 1m", ">1 - 5m", ">5 - 10m", ">10m"]
        )

        operating_cashflow = st.radio(
            "Company's operating cashflow range? (choose one)",
            ["<0", "0 - 100k", "100 - 500k", ">500k - 1m", ">1 - 5m", ">5m"]
        )

        debt_equity_ratio = st.radio(
            "Company's Debt/Equity Ratio (Choose one)",
            ["<0.5", "0.5 - 1.0x", ">1.0 - 3x", ">3x"]
        )

        shareholders_funds = st.radio(
            "Shareholder's funds range? (Choose one)",
            ["<500k", "500k - 1m", "1 - 5m", ">5 - 10m", ">10 - 30m", ">30 - 50m", ">50m"]
        )

        staff_strength = st.radio(
            "Current staff strength (choose one)",
            ["<5", "5 - 10", ">10 - 30", ">30 - 50", ">50 - 80", ">80 - 100", ">100"]
        )

        customer_type = st.radio(
            "My current customers (choose one)",
            ["Only domestic", "Mix of domestic and foreign/off-shore", "Only off-shore"]
        )

        submit = st.form_submit_button("Submit Business Profile")
        if submit:
            if industry == "Others please specify" and not other_industry_details:
                st.error("Please specify your industry if you selected 'Others'.")
                return None
            if incorporation_status == "Others" and not other_incorporation_details:
                st.error("Please specify your incorporation status if you selected 'Others'.")
                return None
            
            return {
                "company_name": company_name,
                "business_model": business_model,
                "products_services": products_services,
                "industry": industry if industry != "Others please specify" else other_industry_details,
                "incorporation_status": incorporation_status if incorporation_status != "Others" else other_incorporation_details,
                "primary_currency": primary_currency,
                "revenue_size": revenue_size,
                "profit_range": profit_range,
                "operating_cashflow": operating_cashflow,
                "debt_equity_ratio": debt_equity_ratio,
                "shareholders_funds": shareholders_funds,
                "staff_strength": staff_strength,
                "customer_type": customer_type
            }
    return None

def render_business_priority_form():
    st.write("### Business Priorities")
    with st.form(key="business_priority_form"):
        business_priorities = st.text_area(
            "Tell me more about your business priorities in the next 6 - 12 months (User Maximum 180 words)",
            max_chars=180,
            height=200
        )
        
        submit = st.form_submit_button("Submit Priorities")
        if submit:
            if not business_priorities.strip():
                st.error("Please provide details about your business priorities.")
                return None
            return {"business_priorities": business_priorities}
    return None

def render_business_options(business_priorities, openai_api_key):
    if 'business_priority_suggestions' not in st.session_state.user_data:
        with st.spinner("Analyzing your business priorities..."):
            suggestions = business_priority(business_priorities, openai_api_key)
            if suggestions:
                st.session_state.user_data['business_priority_suggestions'] = suggestions
    
    if st.session_state.user_data.get('business_priority_suggestions'):
        with st.expander("Business Priority Suggestions", expanded=True):
            st.write("Here are some business priority suggestions based on your input:")
            st.markdown(st.session_state.user_data['business_priority_suggestions'])
    
    st.write("### Business Areas for Analysis")
    st.write("Based on your priorities, select the relevant business areas:")
    
    with st.form(key="business_options_form"):
        selected_options = {}
        cols = st.columns(3)
        
        for idx, (option, description) in enumerate(BUSINESS_OPTIONS.items()):
            col = cols[idx % 3]
            with col:
                with st.expander(f"📊 {option}", expanded=False):
                    st.markdown(f"**{description}**")
                    selected_options[option] = st.checkbox("Select this area", key=f"checkbox_{option}")
        
        submit = st.form_submit_button("💫 Generate Analysis for Selected Areas")
        if submit:
            return selected_options
    return None

def render_working_capital_form():
    st.write("### Working Capital Planning")
    with st.form(key="working_capital_form"):
        funding_amount = st.radio(
            "How much funding do you plan to set aside at present and in the future?",
            options=["<1m", "1 - 5m", "5 - 10m", ">10 - 30m", ">30 - 50m", ">50m"]
        )

        st.write("Purpose of raising funds? (Choose 1 or more)")
        purpose_options = {
            "To expand business operations.": st.checkbox("To expand business operations."),
            "To launch new products or services.": st.checkbox("To launch new products or services."),
            "To pay off existing debts.": st.checkbox("To pay off existing debts."),
            "To invest in technology upgrades.": st.checkbox("To invest in technology upgrades."),
            "To hire and train additional staff.": st.checkbox("To hire and train additional staff."),
            "To enter new markets.": st.checkbox("To enter new markets."),
            "To improve cash flow and working capital.": st.checkbox("To improve cash flow and working capital."),
            "To acquire another company.": st.checkbox("To acquire another company."),
            "To enhance marketing and branding efforts.": st.checkbox("To enhance marketing and branding efforts."),
            "To build inventory and manage supply chain demands.": st.checkbox("To build inventory and manage supply chain demands."),
            "Others please specify": st.checkbox("Others please specify")
        }

        other_purpose = None
        if purpose_options["Others please specify"]:
            other_purpose = st.text_input("Please specify other purposes")

        st.write("Debt or equity preference? (Choose 1 or more)")
        funding_types = {
            "Debt": st.checkbox("Debt", key="funding_type_debt"),
            "Equity": st.checkbox("Equity", key="funding_type_equity"),
            "Both": st.checkbox("Both", key="funding_type_both"),
            "Others please specify": st.checkbox("Others please specify", key="funding_type_others")
        }

        other_funding_type = None
        if funding_types["Others please specify"]:
            other_funding_type = st.text_input("Please specify other funding type")

        submit = st.form_submit_button("Submit Working Capital Plan")
        if submit:
            if purpose_options["Others please specify"] and not other_purpose:
                st.error("Please specify other purposes for raising funds.")
                return None
            if funding_types["Others please specify"] and not other_funding_type:
                st.error("Please specify other funding type.")
                return None
            
            return {
                "funding_amount": funding_amount,
                "funding_purposes": purpose_options,
                "other_purpose": other_purpose,
                "funding_types": funding_types,
                "other_funding_type": other_funding_type
            }
    return None

def render_strategic_planning_form():
    st.write("### Strategic Planning")
    with st.form(key="strategic_planning_form"):
        # Complete list of strategic questions
        strategic_questions = {
            "What best describes your business goal?": [
                "Expanding into new markets",
                "Increasing revenue or profitability",
                "Launching a new product or service",
                "Securing funding or investment"
            ],
            "What key milestone do you prioritize?": [
                "Achieving a specific revenue target",
                "Building a strong brand presence",
                "Creating operational efficiency",
                "Entering a new market"
            ],
            "How would you define your business focus?": [
                "Offering innovative products or services",
                "Meeting a specific customer need",
                "Building a trusted brand in the market",
                "Becoming a market leader in your industry"
            ],
            "What is your unique value proposition?": [
                "Providing unmatched quality",
                "Offering cost-effective solutions",
                "Delivering exceptional customer service",
                "Introducing innovative solutions"
            ],
            "Who is your primary target audience?": [
                "Young professionals or millennials",
                "Small businesses or startups",
                "Large enterprises or corporations",
                "General consumers"
            ],
            "What is your approach to competition?": [
                "Offer better quality at competitive prices",
                "Focus on niche markets competitors overlook",
                "Create superior customer experience",
                "Leverage innovation to stay ahead"
            ],
            "What best describes your organizational structure?": [
                "Flat structure for agility",
                "Hierarchical structure for clear roles",
                "Collaborative teams for innovation",
                "Outsourced or lean operations"
            ],
            "What is your management team's priority?": [
                "Driving innovation and growth",
                "Maintaining operational efficiency",
                "Fostering teamwork and collaboration",
                "Achieving financial targets"
            ],
            "What is the focus of your product/service?": [
                "Solving a specific customer pain point",
                "Offering unique features not available elsewhere",
                "Providing cost savings to customers",
                "Delivering premium quality or value"
            ],
            "What is your product/service strategy?": [
                "Continuously innovate and improve offerings",
                "Expand offerings based on customer needs",
                "Build long-term customer loyalty",
                "Focus on a specific niche market"
            ],
            "What is your primary marketing focus?": [
                "Building brand awareness",
                "Generating leads and conversions",
                "Retaining existing customers",
                "Expanding into new markets"
            ],
            "What is your sales strategy?": [
                "Focus on high-value customers",
                "Drive sales through digital channels",
                "Build relationships through personal engagement",
                "Expand through strategic partnerships"
            ],
            "What is critical to your daily operations?": [
                "Streamlining workflows with technology",
                "Ensuring customer satisfaction",
                "Managing supply chain and logistics",
                "Monitoring financial performance"
            ],
            "Where do you plan to invest operationally?": [
                "Upgrading technology and tools",
                "Expanding team and workforce",
                "Improving facilities or infrastructure",
                "Strengthening supplier relationships"
            ],
            "What is your revenue focus?": [
                "Diversify income streams",
                "Maximize profitability in core areas",
                "Balance steady income with high growth",
                "Secure funding to expand operations"
            ],
            "What is your funding requirement?": [
                "Scaling business operations",
                "Launching new products or services",
                "Expanding market presence",
                "Addressing operational challenges"
            ],
            "What do you see as your primary risk?": [
                "Market competition",
                "Financial uncertainty",
                "Operational inefficiency",
                "Customer retention"
            ],
            "How do you plan to mitigate risks?": [
                "Develop contingency plans",
                "Diversify offerings",
                "Build strong financial reserves",
                "Strengthen customer relationships"
            ]
        }

        # Collect user responses
        responses = {}
        for question, options in strategic_questions.items():
            st.write(question)
            responses[question] = []
            for option in options:
                if st.checkbox(option, key=f"{question}_{option}"):
                    responses[question].append(option)
            st.write("")  # Add spacing between questions

        # Submit button
        submit = st.form_submit_button("Submit Strategic Planning")
        if submit:
            if all(len(responses[q]) > 0 for q in strategic_questions):
                return responses
            else:
                st.error("Please select at least one option for each question.")
    return None

def render_financial_projections_form():
    st.write("### Growth Rate Projections")
    with st.form(key="growth_projections_form"):
        growth_rate = st.radio(
            "What's your average expansion growth rate annually that is sustainable?",
            ["<0%", "1 - 5%", "5 - 10%", ">10 - 30%", ">30 - 50%", ">50 - 100%", ">100 - 500%"],
            key="growth_rate"
        )

        submit = st.form_submit_button("Submit Growth Rate Projection")
        if submit:
            return {
                "growth_rate": growth_rate
            }
    return None

# GPT Processing Functions
def process_business_profile_with_gpt(form_data, api_key):
    prompt = f"""
    Analyze the whole information provided in 1500 words, supported by relevant facts and figures:

    {form_data}

    - Provide a company profile analysis:
        - Include an industry overview with supporting facts and figures, as well as relevant statistics for the industry.
        - Conduct a SWOT analysis based on the provided industry description.
        - Offer a comprehensive financial and operating summary, blending the provided data with macro analysis and the competitive environment.
        - Create an in-depth analysis of the business needs as outlined by the user.

    1..main header comes w summary for that section : 600 words. 
    2. Section header: dedicate and force 2 pages only per section.. means all the sub sections force to 2 pages for that section: 1500 words
    3. Dedicate 1 extra page for that section with a summary table of the key point
    That summary table comes with a basic explanation in 200 words.
    """
    return get_openai_response(
        prompt,
        "You are a business consultant analyzing the business profile data to provide detailed and actionable recommendations.",
        api_key
    )

def process_business_priorities_with_gpt(form_data, api_key):
    prompt = f"""
    Expand and analyze the given points with the following requirements:

    {form_data}

    - Expand the given points and provide a detailed explanation.
    - Synthesize and organize the inputs into a coherent structure.
    - Explain with possible examples or scenarios for better understanding.
    - Provide strategic implications and their potential impact.
    - Ensure the analysis is concise, within 450 words, and supported by relevant facts and figures.

    1..main header comes w summary for that section : 600 words. 
    2. Section header: dedicate and force 2 pages only per section.. means all the sub sections force to 2 pages for that section: 1500 words
    3. Dedicate 1 extra page for that section with a summary table of the key point
    That summary table comes with a basic explanation in 200 words.
    """
    return get_openai_response(
        prompt,
        "You are a strategic consultant providing detailed insights and recommendations based on business priorities.",
        api_key
    )

def business_priority(business_info, openai_api_key):
    prompt = f"""Based on the following business priorities:

{business_info}

Please provide a comprehensive 450-word analysis with the following structure:

1. Expanded Analysis 
   - Break down each priority into key components
   - Identify underlying objectives and goals
   - Highlight critical success factors
   - Discuss potential challenges and constraints

2. Synthesis and Organization 
   - Categorize priorities by strategic importance
   - Identify interconnections between different priorities
   - Create a logical framework for implementation
   - Establish priority hierarchy

3. Practical Examples 
   - For each major priority, provide:
     * A specific implementation example
     * Real-world success case
     * Potential adaptation strategies

4. Strategic Implications 
   - Impact on business operations
   - Resource requirements
   - Timeline considerations
   - Risk assessment
   - Success metrics

Include supporting facts and figures throughout the analysis to validate recommendations and insights.
Ensure all sections include supporting facts, figures, and relevant industry statistics where applicable. 
The analysis should be data-driven and provide actionable insights.
Format all numerical examples in plain text with proper spacing no numbering point"""

    return get_openai_response(
        prompt,
        "You are a strategic business advisor providing comprehensive priority analysis with practical insights and clear examples.",
        openai_api_key
    )

def get_specific_suggestions(business_info, suggestion_type, openai_api_key):
    prompt = f"""Based on the user's stated business priorities:
{business_info}

Provide a {suggestion_type} analysis with exactly these requirements (Maximum 200 words):

1. Explain how to focus energy and resources on activities that directly support your stated priority - give 3 examples 
2. How to develop a clear plan with measurable milestones to ensure consistent progress toward your goal. Highlight and explain the importance of structured goal-setting in the specific context. 
3. Explain how to delegate tasks that do not align with your priority to maintain focus and efficiency - give examples om how to promote  prioritization and productivity.
4. Explain how to Communicate your priorities clearly to your team to ensure alignment and collective action." Provide examples on how to emphasize the value of shared understanding and collaboration.
5. Explain how to Regularly review your progress and adapt your approach to stay aligned with your desired outcomes." Give examples on how to Advocate for continuous evaluation and flexibility in this situation.

Ensure all sections include supporting facts, figures, and relevant industry statistics where applicable. 
The analysis should be data-driven and provide actionable insights.
Format all numerical examples in plain text with proper spacing no numbering point"""

    return get_openai_response(
        prompt,
        f"You are a specialized {suggestion_type} consultant responding to specific business priorities.",
        openai_api_key
    )

def process_working_capital_with_gpt(form_data, api_key):
    prompt = f"""
    Please provide a comprehensive working capital analysis (maximum 600 words) that covers the following key areas:

    1. Working Planning Requirements Summary:
    - Analyze the submitted working capital plan details
    - Provide a concise overview of the key planning elements
    {form_data}

    2. Funding Purpose Analysis:
    - Evaluate the required funding amount in relation to stated purposes
    - Assess whether the funding allocation aligns with business objectives
    - Provide quantitative analysis of funding distribution

    3. Risk Assessment:
    - Identify potential risks associated with each funding purpose
    - Analyze severity and likelihood of identified risks
    - Outline specific risk factors that could impact success

    4. Benefits and Impact Analysis:
    - Detail potential benefits for each funding purpose
    - Quantify expected impact where possible
    - Evaluate both short-term and long-term implications

    1..main header comes w summary for that section : 600 words. 
    2. Section header: dedicate and force 2 pages only per section.. means all the sub sections force to 2 pages for that section: 1500 words
    3. Dedicate 1 extra page for that section with a summary table of the key point
    That summary table comes with a basic explanation in 200 words.
    """
    
    return get_openai_response(
        prompt,
        "You are a financial analyst specializing in working capital management, providing detailed analysis and recommendations based on submitted plan data.",
        api_key
    )

def process_strategic_planning_with_gpt(form_data, api_key):
    prompt = f"""
    Provide a comprehensive strategic business analysis based on the following planning data:

    {form_data}

    1. Business Strategy Assessment:
    - Analyze the alignment between stated business goals and target audience
    - Evaluate the coherence of value proposition with market positioning
    - Assess the relationship between product/service strategy and revenue focus

    2. Operational & Resource Analysis:
    - Examine the alignment of organizational structure with management priorities
    - Evaluate operational investment plans against critical daily needs
    - Analyze the connection between funding requirements and planned investments

    3. Market & Competition Strategy:
    - Assess the effectiveness of marketing and sales strategies for the target audience
    - Evaluate competitive approach in relation to unique value proposition
    - Analyze market expansion plans and potential barriers

    4. Risk Management & Sustainability:
    - Identify potential conflicts between different strategic elements
    - Evaluate the comprehensiveness of risk mitigation strategies
    - Assess the long-term sustainability of the proposed strategies

    5. Recommendations:
    - Provide specific, actionable recommendations for strategy optimization
    - Identify quick wins and long-term strategic initiatives
    - Suggest performance metrics for tracking strategic success

    1..main header comes w summary for that section : 600 words. 
    2. Section header: dedicate and force 2 pages only per section.. means all the sub sections force to 2 pages for that section: 1500 words
    3. Dedicate 1 extra page for that section with a summary table of the key point
    That summary table comes with a basic explanation in 200 words.
    """
    
    return get_openai_response(
        prompt,
        "You are a strategic business consultant specializing in comprehensive business strategy analysis, providing detailed insights and actionable recommendations based on submitted strategic planning data.",
        api_key
    )

def process_financial_projections_with_gpt(form_data, company_data, api_key):
    """Generate 5-year financial projections"""
    prompt = f"""
    Based on the company's historical data:
    Annual Revenue Size: {company_data['business_profile'].get('revenue_size')}
    Profit Range: {company_data['business_profile'].get('profit_range')}
    Operating Cashflow Range: {company_data['business_profile'].get('operating_cashflow')}
    Debt/Equity Ratio: {company_data['business_profile'].get('debt_equity_ratio')}
    Shareholder's Funds Levels: {company_data['business_profile'].get('shareholders_funds')}
    Growth Rate Selected: {form_data['growth_rate']}

    Please extrapolate and provide detailed 5-year financial projections with the following requirements:
    Use these projected expansion growth rate (annually)  to extrapolate their topline and bottom line annually in the next 5 years , BASED ON THE COMPANY'S DATA PROVIDED EARLIER
    
    Based on the 5-year projections and company profile, provide a 600-word narrative analysis listing and explaining at least 8 risk assumptions:
    List and explain at least 8 risk assumptions to the financial projections in 600 words narratively.
    Format as a narrative discussion with clear sections for each risk.

    Create a table based on these financial projections and data provided earlier - using both qualitative and quantitative data provided. 
    Link these numbers to the business strategy of the company.
    State and explain the growth assumptions narratively in 700 words with supporting facts, figures in % and $ terms, with reference to time frame. 
    """
    return get_openai_response(
        prompt,
        "You are a financial analyst creating detailed 5-year projections based on historical company data and growth assumptions.",
        api_key
    )
def get_business_option_summary(selected_areas, suggestions_data, openai_api_key):
    """
    Create a high-level summary of all selected business options and their suggestions.
    
    Args:
        selected_areas (list): List of selected business options
        suggestions_data (dict): Dictionary containing the detailed suggestions for each area
        openai_api_key (str): OpenAI API key for generating the summary
    
    Returns:
        str: A concise summary of all selected areas and key recommendations
    """
    # Create a consolidated view of all selected areas and their suggestions
    consolidated_info = "\n\n".join([
        f"Area: {area}\n"
        f"Description: {BUSINESS_OPTIONS[area]}\n"
        f"Detailed Analysis: {suggestions_data.get(f'{area.lower().replace(' ', '_')}_analysis', 'No analysis available')}"
        for area in selected_areas
    ])
    
    prompt = f"""Based on the following selected business areas and their detailed analyses, 
    provide a concise executive summary:

    {consolidated_info}

    Please provide a summary that includes:
    1. Overview of selected focus areas and their strategic importance
    2. Key synergies between the different areas
    3. Critical success factors across all areas
    4. Top 3-5 immediate action items
    5. Potential challenges and mitigation strategies

    1..main header comes w summary for that section : 600 words. 
    2. Section header: dedicate and force 2 pages only per section.. means all the sub sections force to 2 pages for that section: 1500 words
    3. Dedicate 1 extra page for that section with a summary table of the key points
    That summary table comes with a basic explanation in 200 words"""

    return get_openai_response(
        prompt,
        "You are a strategic business consultant providing executive-level summaries. Focus on practical, actionable insights.",
        openai_api_key
    )
class PDFWithTOC(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        self.personal_info = kwargs.get('personal_info', {})
        if 'personal_info' in kwargs:
            del kwargs['personal_info']
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        self.page_numbers = {}
        self.current_page = 1

    def afterPage(self):
        self.current_page += 1

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            if style == 'heading':
                text = flowable.getPlainText()
                self.page_numbers[text] = self.current_page

def generate_pdf(sme_data, personal_info, toc_page_numbers):
    buffer = io.BytesIO()
    
    doc = PDFWithTOC(
        buffer,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=1.5*inch,
        bottomMargin=inch,
        personal_info=personal_info
    )
    
    full_page_frame = Frame(
        0, 0, letter[0], letter[1],
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0
    )
    
    normal_frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id='normal'
    )
    
    disclaimer_frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id='disclaimer'
    )
    
    templates = [
        PageTemplate(id='First', frames=[full_page_frame],
                    onPage=lambda canvas, doc: None),
        PageTemplate(id='Later', frames=[normal_frame],
                    onPage=create_header_footer),
        PageTemplate(id='dis', frames=[normal_frame],
                    onPage=create_header_footer_disclaimer)
    ]
    doc.addPageTemplates(templates)
    
    styles = create_custom_styles()
    elements = []
    
    # Cover page
    elements.append(NextPageTemplate('First'))
    if os.path.exists("smeboostfront.jpg"):
        img = Image("smeboostfront.jpg", width=letter[0], height=letter[1])
        elements.append(img)
    
    elements.append(NextPageTemplate('Later'))
    elements.append(PageBreak())
    
    # Table of Contents
    elements.append(Paragraph("Table of Contents", styles['heading']))
    
    # Section data
    section_data = [
        ("Company Profile Analysis", sme_data['business_profile_analysis']),
        ("Business Priorities Analysis", sme_data['priorities_analysis']),
        ("Business Options Summary", sme_data['executive_summary']),
        ("Working Capital Analysis", sme_data['capital_analysis']),
        # ("Strategic Planning Analysis", sme_data['strategic_analysis']),
        ("Financial Projections", sme_data['financial_projections'])
    ]
    
    # Format TOC entries
    toc_style = ParagraphStyle(
        'TOCEntry',
        parent=styles['normal'],
        fontSize=12,
        leading=20,
        leftIndent=20,
        rightIndent=30,
        spaceBefore=10,
        spaceAfter=10,
        fontName='Helvetica'
    )
    styles['toc'] = toc_style

    def create_toc_entry(num, title, page_num):
        title_with_num = f"{num}. {title}"
        dots = '.' * (50 - len(title_with_num))
        return f"{title_with_num} {dots} {page_num}"

    # Add static Personal Profile entry
    static_entry = create_toc_entry(1, "Personal Profile", 3)
    elements.append(Paragraph(static_entry, toc_style))

    # Add dynamic entries for other sections
    for i, ((title, _), page_num) in enumerate(zip(section_data, toc_page_numbers), 2):
        toc_entry = create_toc_entry(i, title, page_num)
        elements.append(Paragraph(toc_entry, toc_style))
    
    elements.append(PageBreak())
    
    # Personal Profile Page
    elements.extend(create_profile_page(styles, personal_info))
    elements.append(PageBreak())
    
    # Main content sections
    for title, content in section_data:
        elements.append(Paragraph(title, styles['heading']))
        process_content(content, styles, elements)
        elements.append(PageBreak())
    
    # Disclaimer
    elements.append(NextPageTemplate('dis'))
    elements.append(PageBreak())
    create_disclaimer_page(styles, elements)
    
    # Back cover
    elements.append(NextPageTemplate('First'))
    elements.append(PageBreak())
    if os.path.exists("smeboostback.png"):
        img = Image("smeboostback.png", width=letter[0], height=letter[1])
        elements.append(img)
    
    doc.build(elements, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer

def create_profile_page(styles, personal_info):
    elements = []
    elements.append(Spacer(1, 0.5*inch))
    
    title_table = Table(
        [[Paragraph("Personal Profile", styles['heading'])]],
        colWidths=[7*inch],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ])
    )
    elements.append(title_table)
    
    elements.append(Spacer(0.5, 0.1*inch))
    
    # Profile info table
    info_table = Table(
        [
            [Paragraph("Contact Information", styles['subheading'])],
            [Table(
                [
                    ["Full Name", str(personal_info.get('full_name', 'N/A'))],
                    ["Email", str(personal_info.get('email', 'N/A'))],
                    ["Phone", str(personal_info.get('phone', 'N/A'))],
                    ["Report Date", datetime.datetime.now().strftime('%B %d, %Y')],
                    ["Report ID", f"SME-{str(uuid.uuid4())[:8]}"]
                ],
                colWidths=[1.5*inch, 4.5*inch],
                style=TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ])
            )]
        ],
        colWidths=[6*inch],
        style=TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ])
    )
    
    elements.append(info_table)
    return elements
from reportlab.platypus import Frame, PageTemplate, BaseDocTemplate, PageBreak
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, NextPageTemplate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if hasattr(self, '_pageNumber'):
            self.setFont("Helvetica", 9)
            self.drawRightString(
                letter[0] - 0.5*inch,
                0.5*inch,
                f"Page {self._pageNumber} of {page_count}"
            )

def create_header_footer(canvas, doc):
    """Add header and footer with company logos and page numbers"""
    canvas.saveState()
    
    if doc.page > 1:  # Only show on pages after the first page
        # Header logos positioning
        x_start = doc.width + doc.leftMargin - 1.0 * inch
        y_position = doc.height + doc.topMargin - 0.1 * inch
        image_width = 0.5 * inch
        image_height = 0.5 * inch

        # Draw logos if available
        for img_name in ["ceai.png", "raa.png", "emma.png"]:
            if os.path.exists(img_name):
                canvas.drawImage(
                    img_name,
                    x_start - (image_width + 0.1 * inch),
                    y_position,
                    width=image_width,
                    height=image_height,
                    mask="auto"
                )
                x_start -= (image_width + 0.1 * inch)
        
        # Get company name from business_profile if available
        if hasattr(doc, 'personal_info') and isinstance(doc.personal_info, dict):
            if 'company_name' in doc.personal_info:
                company_name = doc.personal_info['company_name']
            else:
                # Try to get from business_profile in session state
                import streamlit as st
                company_name = st.session_state.get('business_profile', {}).get('company_name', '')
        else:
            company_name = ''

        # Add Header Text
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(
            doc.leftMargin,
            doc.height + doc.topMargin - 0.1*inch,
            company_name
        )
        
        # Add line below header
        line_y_position = doc.height + doc.topMargin - 0.35 * inch
        canvas.setLineWidth(0.5)
        canvas.line(
            doc.leftMargin,
            line_y_position,
            doc.width + doc.rightMargin,
            line_y_position
        )
        
        # Footer
        canvas.setFont("Helvetica", 9)
        canvas.drawString(
            doc.leftMargin,
            0.5 * inch,
            f"Generated on {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        )
    
    canvas.restoreState()

def create_header_footer_disclaimer(canvas, doc):
    """Add header and footer for disclaimer page"""
    canvas.saveState()
    
    if doc.page > 1:
        # Header logos positioning
        x_start = doc.width + doc.leftMargin - 1.0 * inch
        y_position = doc.height + doc.topMargin - 0.1 * inch
        image_width = 0.5 * inch
        image_height = 0.5 * inch

        # Draw logos
        for img_name in ["ceai.png", "raa.png", "emma.png"]:
            if os.path.exists(img_name):
                canvas.drawImage(
                    img_name,
                    x_start - (image_width + 0.1 * inch),
                    y_position,
                    width=image_width,
                    height=image_height,
                    mask="auto"
                )
                x_start -= (image_width + 0.1 * inch)
        
        # Header Text
        canvas.setFont("Helvetica-Bold", 27)
        canvas.drawString(
            doc.leftMargin,
            doc.height + doc.topMargin - 0.1*inch,
            "Disclaimer"
        )

        # Line below header
        canvas.setLineWidth(0.5)
        canvas.line(
            doc.leftMargin,
            doc.height + doc.topMargin - 0.30 * inch,
            doc.width + doc.rightMargin,
            doc.height + doc.topMargin - 0.30 * inch
        )

        # Footer
        canvas.setFont("Helvetica", 9)
        canvas.drawString(
            doc.leftMargin,
            0.5 * inch,
            f"Generated on {datetime.datetime.now().strftime('%B %d, %Y')}"
        )
        canvas.drawRightString(
            doc.width + doc.rightMargin,
            0.5 * inch,
            f"Page {doc.page}"
        )
    
    canvas.restoreState()

def create_disclaimer_page(styles, elements):
    """Create disclaimer page content"""
    # Register Lato fonts if available
    try:
        pdfmetrics.registerFont(TTFont('Lato', 'fonts/Lato-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('Lato-Bold', 'fonts/Lato-Bold.ttf'))
        base_font = 'Lato'
        bold_font = 'Lato-Bold'
    except:
        base_font = 'Helvetica'
        bold_font = 'Helvetica-Bold'
    
    # Disclaimer styles
    disclaimer_styles = {
        'section_header': ParagraphStyle(
            'SectionHeader',
            parent=styles['normal'],
            fontSize=12,
            fontName=bold_font,
            spaceBefore=12,
            spaceAfter=6,
        ),
        'body_text': ParagraphStyle(
            'BodyText',
            parent=styles['normal'],
            fontSize=10,
            fontName=base_font,
            leading=14,
            alignment=TA_JUSTIFY
        )
    }

    # Add disclaimer sections
    elements.append(Paragraph("Report Disclaimer and Limitations", disclaimer_styles['section_header']))
    
    disclaimer_text = """
    This report has been generated using artificial intelligence and data analysis tools. While we strive to provide accurate and helpful information, please note the following limitations:

    1. The analyses and recommendations provided are based on the information submitted and available at the time of generation.
    2. Financial projections and business analyses should be used as guidance only and validated with professional advisors.
    3. Market conditions and business environments can change rapidly, affecting the relevance of recommendations.
    4. This report should not be considered as financial, legal, or professional advice.
    5. Users should exercise their own judgment and consult with relevant professionals before making business decisions.
    """
    
    elements.append(Paragraph(disclaimer_text, disclaimer_styles['body_text']))
    elements.append(Spacer(1, 0.2*inch))

    # Add confidentiality notice
    elements.append(Paragraph("Confidentiality Notice", disclaimer_styles['section_header']))
    
    confidentiality_text = """
    This document contains confidential and proprietary information. The content should not be shared or distributed without proper authorization. All rights reserved.
    """
    
    elements.append(Paragraph(confidentiality_text, disclaimer_styles['body_text']))
def process_content(content, styles, elements):
    """Process content with proper formatting"""
    if not content:
        return
    
    # Handle case where content is a dictionary
    if isinstance(content, dict):
        for title, analysis in content.items():
            elements.append(Paragraph(title, styles['subheading']))
            if isinstance(analysis, str):
                paragraphs = analysis.strip().split('\n')
                for para in paragraphs:
                    process_paragraph(para, styles, elements)
            elements.append(Spacer(1, 0.2*inch))
        return

    # Define all possible section headers from various prompts
    section_headers = [
        "Company Profile Analysis",
        "Industry Overview",
        "SWOT Analysis",
        "Financial and Operating Summary",
        "Business Needs Analysis",
        "Expanded Analysis",
        "Synthesis and Organization",
        "Practical Examples",
        "Strategic Implications",
        "Working Capital Planning",
        "Amount vs Purpose Analysis",
        "Risk Assessment",
        "Benefits Analysis",
        "Eligibility Status",
        "Detailed Analysis of Unmet Criteria",
        "Eligibility Score",
        "Advisor/Coach Need Analysis",
        "Targeted Solutions",
        "KPI Timeline Breakdown",
        "Benefits and Impact Analysis",
        "Potential Impact on Financing Eligibility",
        "Potential Challenges and Mitigation Strategies",
        "Funding Request",
        "Business Profile",
        "Detailed Criteria Analysis",
        "Financial Profile",
        "Recommendations",
        "Competitive Landscape",
        "Industry Statistics and Benchmarks",
        "Market Size and Trends",
        "Working Planning Requirements Summary",
        "Forward Looking Quote"
    ]

    # Split content into sections
    sections = content.split('\n\n')
    
    for section in sections:
        lines = section.strip().split('\n')
        first_line = lines[0].strip()
        
        # Remove any Markdown formatting and special characters
        first_line = re.sub(r'^[#\s*]+', '', first_line)  # Remove leading #, spaces, asterisks
        first_line = re.sub(r'[\*:]$', '', first_line)    # Remove trailing asterisks and colons
        first_line = first_line.strip()
        
        # Remove numbers at the start
        first_line = re.sub(r'^\d+\.\s*', '', first_line)
        
        # Check if this is a header
        is_header = any(header.lower() in first_line.lower() for header in section_headers)
        
        if is_header:
            # Clean up the header text
            header = first_line.strip()
            # Remove any remaining special characters or formatting
            header = re.sub(r'[*_:#]', '', header).strip()
            
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(header, styles['subheading']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Process remaining lines in the section
            if len(lines) > 1:
                for para in lines[1:]:
                    if para.strip():
                        process_paragraph(para, styles, elements)
        else:
            # Process as regular paragraph
            for para in lines:
                if para.strip():
                    process_paragraph(para, styles, elements)
    
    # Split content into sections
    sections = content.split('\n\n')
    in_table = False
    table_data = []
    
    for section in sections:
        lines = section.strip().split('\n')
        if not lines:
            continue
            
        # Check if this section contains a table
        if any('|' in line for line in lines):
            # Process table content
            table_data = []
            for line in lines:
                if '|' in line and '-|-' not in line:  # Skip separator lines
                    cells = [cell.strip() for cell in line.split('|')]
                    # Remove empty cells from start/end
                    cells = [cell for cell in cells if cell]
                    if cells:  # Only add non-empty rows
                        table_data.append(cells)
            
            if table_data:
                # Create and format table
                table = create_formatted_table(table_data, styles)
                elements.append(Spacer(1, 0.2*inch))
                elements.append(table)
                elements.append(Spacer(1, 0.2*inch))
            continue
        
        # Process non-table content
        for line in lines:
            if line.strip():
                elements.append(Paragraph(line.strip(), styles['content']))
                elements.append(Spacer(1, 0.1*inch))

    return elements
def process_paragraph(para, styles, elements):
    """Process individual paragraph with formatting"""
    clean_para = clean_text(para)
    if not clean_para:
        return
    
    # Handle bullet points and dashes
    if clean_para.startswith(('•', '-', '*')):
        text = clean_para.lstrip('•-* ').strip()
        elements.append(Paragraph(f"• {text}", styles['bullet']))
    
    # Handle numbered points
    elif re.match(r'^\d+\.?\s+', clean_para):
        text = re.sub(r'^\d+\.?\s+', '', clean_para)
        elements.extend([
            Spacer(1, 0.1*inch),
            create_highlight_box(text, styles),
            Spacer(1, 0.1*inch)
        ])
    
    # Handle scores and metrics
    elif "Overall Score:" in clean_para:
        # Remove asterisks and preserve the score
        text = clean_para.replace('**', '').strip()
        elements.append(Paragraph(text, styles['content']))
    
    # Handle quoted text
    elif clean_para.strip().startswith('"') and clean_para.strip().endswith('"'):
        quote_style = ParagraphStyle(
            'Quote',
            parent=styles['content'],
            fontSize=24,  # Increased from 18 to 24 for bigger text
            leftIndent=20,
            rightIndent=20,
            leading=28,   # Increased leading (line height) to match larger font
            textColor=colors.black  # Added to make text black
        )
        elements.append(Paragraph(clean_para, quote_style))
        elements.append(Spacer(1, 0.1*inch))
    
    else:
        # Normal black text for everything else
        elements.append(Paragraph(clean_para, styles['content']))
        elements.append(Spacer(1, 0.05*inch))
def create_custom_styles():
    base_styles = getSampleStyleSheet()
    
    try:
        pdfmetrics.registerFont(TTFont('Lato', 'fonts/Lato-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('Lato-Bold', 'fonts/Lato-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('Lato-Italic', 'fonts/Lato-Italic.ttf'))
        pdfmetrics.registerFont(TTFont('Lato-BoldItalic', 'fonts/Lato-BoldItalic.ttf'))
        base_font = 'Lato'
        bold_font = 'Lato-Bold'
    except:
        base_font = 'Helvetica'
        bold_font = 'Helvetica-Bold'

    styles = {
        'Normal': base_styles['Normal'],
        'TOCEntry': ParagraphStyle(
            'TOCEntry',
            parent=base_styles['Normal'],
            fontSize=12,
            leading=16,
            leftIndent=20,
            fontName=base_font,
            alignment=TA_JUSTIFY  # Add this line
        ),
        'title': ParagraphStyle(
            'CustomTitle',
            parent=base_styles['Normal'],
            fontSize=24,
            textColor=colors.HexColor('#2B6CB0'),
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName=bold_font,
            leading=28.8
        ),
        'heading': ParagraphStyle(
            'CustomHeading',
            parent=base_styles['Normal'],
            fontSize=26,
            textColor=colors.HexColor('#1a1a1a'),
            spaceBefore=20,
            spaceAfter=15,
            fontName=bold_font,
            leading=40.5,
            tracking=0,
            alignment=TA_JUSTIFY  # Add this line
        ),
        'subheading': ParagraphStyle(
            'CustomSubheading',
            parent=base_styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#4A5568'),
            spaceBefore=15,
            spaceAfter=10,
            fontName=bold_font,
            leading=18.2,
            alignment=TA_JUSTIFY  # Add this line
        ),
        'normal': ParagraphStyle(
            'CustomNormal',
            parent=base_styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1a1a1a'),
            spaceBefore=6,
            spaceAfter=6,
            fontName=base_font,
            leading=15.4,
            tracking=0,
            alignment=TA_JUSTIFY  # Add this line
        ),
        'content': ParagraphStyle(
            'CustomContent',
            parent=base_styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1a1a1a'),
            alignment=TA_JUSTIFY,  # This was already correct
            spaceBefore=6,
            spaceAfter=6,
            fontName=base_font,
            leading=15.4,
            tracking=0
        ),
        'bullet': ParagraphStyle(
            'CustomBullet',
            parent=base_styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1a1a1a'),
            leftIndent=20,
            firstLineIndent=0,
            fontName=base_font,
            leading=15.4,
            tracking=0,
            alignment=TA_JUSTIFY  # Add this line
        )
    }
    
    return styles
def create_formatted_table(table_data, styles):
    """Create a professionally formatted table with consistent styling"""
    from reportlab.lib import colors
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib.units import inch
    
    # Ensure all rows have the same number of columns
    max_cols = max(len(row) for row in table_data)
    table_data = [row + [''] * (max_cols - len(row)) for row in table_data]
    
    # Calculate column widths based on content
    total_width = 6.5 * inch  # Standard letter page width minus margins
    if max_cols > 1:
        # First column slightly narrower, remaining columns share space evenly
        col_widths = [2*inch] + [(total_width - 2*inch)/(max_cols-1)] * (max_cols-1)
    else:
        col_widths = [total_width]
    
    # Create table with calculated widths
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    # Define professional table style
    style = TableStyle([
        # Header row styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F3F4F6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Content styling
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        
        # Grid styling
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        
        # Alignment
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Cell padding
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ])
    
    # Apply word wrapping to all cells
    for row in range(len(table_data)):
        for col in range(len(table_data[0])):
            if table_data[row][col]:
                wrapped_text = Paragraph(table_data[row][col], styles['content'])
                table_data[row][col] = wrapped_text
    
    table.setStyle(style)
    return table
def clean_text(text):
    """Clean and format text by removing unwanted formatting"""
    if not text:
        return ""
    
    # Remove style tags
    text = re.sub(r'<userStyle>.*?</userStyle>', '', text)
    
    # Remove Markdown formatting without affecting content
    text = text.replace('**', '')  # Remove bold markers
    text = text.replace('*', '')   # Remove italic markers
    text = text.replace('_', '')   # Remove underscore
    text = text.replace(':', ': ') # Add space after colons
    
    # Remove Markdown headers while preserving text
    text = re.sub(r'^#+\s*', '', text)
    
    # Clean up multiple spaces and preserve paragraph structure
    text = ' '.join(text.split())
    
    return text.strip()

def create_highlight_box(text, styles):
    """Create highlighted box with consistent styling"""
    return Table(
        [[Paragraph(f"• {text}", styles['content'])]],
        colWidths=[6*inch],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
            ('BORDER', (0,0), (-1,-1), 1, colors.HexColor('#90CDF4')),
            ('PADDING', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ])
    )
# Main Function
def main():
    initialize_session_state()
    render_header()

    # Store API key in session state
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ''
    
    # Get API key input
    api_key_input = st.text_input("OpenAI API Key", type="password", value=st.session_state.openai_api_key)
    
    if api_key_input:
        st.session_state.openai_api_key = api_key_input
    
    if not st.session_state.openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")
        return

    st.write("The SMEBoost Lite GenAI platform is a streamlined, AI-powered version of the full SMEBoost program...")

    # Step 0: Personal Profile
    if "personal_profile" not in st.session_state:
        st.write("## Personal Profile")
        personal_profile = render_personal_profile_form()
        if personal_profile:
            st.session_state["personal_profile"] = personal_profile
            st.success("Personal profile submitted successfully!")
        else:
            st.stop()

    # Step 1: Business Profile
    if "business_profile" not in st.session_state:
        st.write("## Step 1: Business Profile")
        business_profile = render_business_profile_form()
        if business_profile:
            st.session_state["business_profile"] = business_profile
            profile_analysis = process_business_profile_with_gpt(business_profile, st.session_state.openai_api_key)
            if profile_analysis:
                st.session_state["business_profile_analysis"] = profile_analysis
                st.success("Business profile submitted successfully!")
                with st.expander("View Business Profile Analysis"):
                    st.markdown(profile_analysis)
        else:
            st.stop()

    # Step 2: Business Priorities
    if "business_priorities" not in st.session_state:
        st.write("## Step 2: Business Priorities")
        business_priorities = render_business_priority_form()
        if business_priorities:
            st.session_state["business_priorities"] = business_priorities
            priorities_analysis = process_business_priorities_with_gpt(business_priorities, st.session_state.openai_api_key)
            if priorities_analysis:
                st.session_state["priorities_analysis"] = priorities_analysis
                st.success("Business priorities submitted successfully!")
                with st.expander("View Business Priorities Analysis"):
                    st.markdown(priorities_analysis)
        else:
            st.stop()

    # Step 3: Business Options
    if "business_options" not in st.session_state:
        st.write("## Step 3: Business Options")
        selected_options = render_business_options(
            st.session_state["business_priorities"], 
            st.session_state.openai_api_key
        )
        if selected_options:
            selected_areas = [opt for opt, selected in selected_options.items() if selected]
            if selected_areas:
                st.session_state["business_options"] = selected_areas
                for option in selected_areas:
                    with st.expander(f"View Analysis for {option}"):
                        suggestion = get_specific_suggestions(
                            st.session_state["business_priorities"], 
                            option, 
                            st.session_state.openai_api_key
                        )
                        if suggestion:
                            # st.markdown("#### Overview")
                            # st.markdown(f"*{BUSINESS_OPTIONS[option]}*")
                            # st.markdown("#### Detailed Analysis")
                            # st.markdown(suggestion)
                            st.session_state[f"{option.lower().replace(' ', '_')}_analysis"] = suggestion

                executive_summary = get_business_option_summary(
                    selected_areas,
                    st.session_state.user_data,
                    st.session_state.openai_api_key
                )
                if executive_summary:
                    st.session_state["executive_summary"] = executive_summary
                    with st.expander("Business Priorities Summary"):
                        st.markdown(executive_summary)
                st.success("Business options analyzed successfully!")
        else:
            st.stop()

    # Step 4: Working Capital
    if "working_capital" not in st.session_state:
        st.write("## Step 4: Working Capital")
        working_capital = render_working_capital_form()
        if working_capital:
            st.session_state["working_capital"] = working_capital
            capital_analysis = process_working_capital_with_gpt(working_capital, st.session_state.openai_api_key)
            if capital_analysis:
                st.session_state["capital_analysis"] = capital_analysis
                st.success("Working capital plan submitted successfully!")
                with st.expander("View Working Capital Analysis"):
                    st.markdown(capital_analysis)
        else:
            st.stop()

    # Step 5: Strategic Planning
    if "strategic_planning" not in st.session_state:
        st.write("## Step 5: Strategic Planning")
        strategic_planning = render_strategic_planning_form()
        if strategic_planning:
            st.session_state["strategic_planning"] = strategic_planning
            strategic_analysis = process_strategic_planning_with_gpt(strategic_planning, st.session_state.openai_api_key)
            if strategic_analysis:
                st.session_state["strategic_analysis"] = strategic_analysis
                st.success("Strategic planning submitted successfully!")
                # with st.expander("View Strategic Planning Analysis"):
                #     st.markdown(strategic_analysis)
        else:
            st.stop()

    # Step 6: Growth Rate Projections
    if "growth_projections" not in st.session_state:
        st.write("## Step 6: Growth Rate Projections")
        growth_projections = render_financial_projections_form()
        if growth_projections:
            st.session_state["growth_projections"] = growth_projections
            company_data = {
                "business_profile": st.session_state.get("business_profile", {}),
                "business_priorities": st.session_state.get("business_priorities", {}),
                "business_options": st.session_state.get("business_options", []),
                "working_capital": st.session_state.get("working_capital", {}),
                "strategic_planning": st.session_state.get("strategic_planning", {})
            }
            
            financial_projections = process_financial_projections_with_gpt(
                growth_projections, 
                company_data, 
                st.session_state.openai_api_key
            )
            if financial_projections:
                st.session_state["financial_projections"] = financial_projections
                st.success("Financial projections completed successfully!")
                with st.expander("View Financial Projections"):
                    st.markdown(financial_projections)
        else:
            st.stop()

    # Show Generate Report button only when all steps are completed
    if all(key in st.session_state for key in [
        "personal_profile", "business_profile", "business_priorities",
        "business_options", "working_capital", "strategic_planning",
        "growth_projections", "business_profile_analysis", "priorities_analysis",
        "capital_analysis", "strategic_analysis", "financial_projections",
        "executive_summary"
    ]):
        st.write("## Generate Final Report")
        if st.button("Generate Complete Report"):
            with st.spinner("Generating PDF Report..."):
# In the PDF generation section of main():
                try:
                    sme_data = {
                        'business_profile_analysis': st.session_state['business_profile_analysis'],
                        'priorities_analysis': st.session_state['priorities_analysis'],
                        'executive_summary': st.session_state['executive_summary'],
                        'capital_analysis': st.session_state['capital_analysis'],
                        'strategic_analysis': st.session_state['strategic_analysis'],
                        'financial_projections': st.session_state['financial_projections']
                    }
                    
                    # Include company name in personal_info
                    personal_info = st.session_state["personal_profile"].copy()
                    personal_info['company_name'] = st.session_state.get('business_profile', {}).get('company_name', '')
                    
                    page_numbers = [4, 6, 8, 10, 12, 14]
                    pdf_buffer = generate_pdf(sme_data, personal_info, page_numbers)
                    
                    st.download_button(
                        "📥 Download SME Analysis Report",
                        data=pdf_buffer,
                        file_name=f"sme_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        help="Click to download your complete SME analysis report"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
                    print(f"Detailed error: {str(e)}")

if __name__ == "__main__":
    main()
