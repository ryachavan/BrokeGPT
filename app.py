import streamlit as st
import re
from datetime import datetime
import json

# Knowledge Base
KNOWLEDGE_BASE = {
    "taxation": {
        "keywords": ["tax", "income tax", "gst", "tds", "deduction", "refund", "filing", "return", "itr", "pan", "section 80c", "advance tax", "tax regime", "slab"],
        "responses": {
            "calculate_tax": """Great question! Let me break down income tax calculation for you step by step.

**Understanding the Process:**

Income tax isn't as scary as it sounds. Think of it like a recipe - you need the right ingredients (your income sources) and follow the steps to get to the final amount.

**Step 1: Calculate Your Gross Total Income**
Add up ALL your income from:
- Salary (including bonuses, allowances)
- House property (rental income)
- Business or profession
- Capital gains (from selling property, stocks, etc.)
- Other sources (interest from savings, FDs, etc.)

**Step 2: Claim Your Deductions**
This is where you can reduce your taxable income! Subtract:
- Standard deduction: ₹50,000 (for salaried individuals)
- Section 80C: Up to ₹1.5 lakh (PPF, ELSS, life insurance, etc.)
- Section 80D: Up to ₹25,000-₹100,000 (health insurance)
- Section 80CCD(1B): Additional ₹50,000 (NPS)
- Home loan interest: Up to ₹2 lakh

**Note:** These deductions are only available in the **Old Tax Regime**!

**Step 3: Choose Your Tax Regime**

**🔹 New Tax Regime (FY 2024-25):**
- Up to ₹3 lakh: **Nil** (completely tax-free!)
- ₹3-7 lakh: **5%**
- ₹7-10 lakh: **10%**
- ₹10-12 lakh: **15%**
- ₹12-15 lakh: **20%**
- Above ₹15 lakh: **30%**

No deductions allowed (simpler but might cost more if you invest a lot).

**🔹 Old Tax Regime:**
- Up to ₹2.5 lakh: **Nil**
- ₹2.5-5 lakh: **5%**
- ₹5-10 lakh: **20%**
- Above ₹10 lakh: **30%**

All deductions (80C, 80D, etc.) are allowed here.

**Step 4: Apply Tax Rebate**
- Section 87A: If your total income is up to ₹7 lakh (new regime) or ₹5 lakh (old regime), you get a rebate making your tax **zero**!

**Step 5: Add Health & Education Cess**
Add 4% cess on your calculated tax amount.

**Quick Example:**
Annual salary: ₹10 lakh
- New Regime: Nil on ₹3L + 5% on ₹4L + 10% on ₹3L = ₹50,000 + cess = ₹52,000
- Old Regime: After ₹1.5L deductions (80C), taxable = ₹8.5L
  Tax: Nil on ₹2.5L + 5% on ₹2.5L + 20% on ₹3.5L = ₹82,500 + cess = ₹85,800

**Pro Tip:** Use the new regime if you don't have many deductions. Otherwise, stick with old!

Need help choosing between regimes? Just ask! 😊""",
            
            "filing_documents": """Ah, the document checklist - let me walk you through everything you'll need!

**📋 Essential Documents for ITR Filing:**

Think of this as your "tax filing survival kit". Missing even one document can delay your refund, so let's make sure you have everything.

**1. Identity & Basic Documents:**
- **PAN Card** - Your tax identity (mandatory!)
- **Aadhaar Card** - For e-verification
- **Bank Account Details** - For refund credit (account number, IFSC code)

**2. Income-Related Documents:**

**If you're salaried:**
- **Form 16** - This is THE most important document from your employer
  - Part A: Shows TDS deducted
  - Part B: Shows salary breakup
- **Salary slips** (all 12 months) - Keep them handy for cross-checking

**If you have other income:**
- **Interest Certificates** - From banks/post office (FD, savings interest)
- **Form 26AS** - Auto-generated statement showing all your income & TDS
- **Form 16A** - For TDS on non-salary income
- **Capital Gains Statement** - From broker (if you trade stocks/mutual funds)

**3. Deduction Proof Documents:**

These help you save tax in the old regime:

**Section 80C (up to ₹1.5 lakh):**
- PPF/EPF statements
- Life insurance premium receipts
- ELSS mutual fund statements
- Children's tuition fee receipts
- Home loan principal certificate

**Section 80D (Health Insurance):**
- Health insurance premium receipts
- Preventive health check-up bills

**Home Loan Benefits:**
- Interest certificate from bank (for 80EE/24b)
- Principal repayment statement (for 80C)

**Other Deductions:**
- NPS statements (80CCD)
- Education loan interest certificate (80E)
- Donations receipts (80G)

**4. Additional Documents:**

- **Form 26AS/AIS** - Download from income tax portal to verify all income
- **Previous year's ITR** - For reference
- **Property documents** - If you own rental property

**🔍 Pro Tips:**

1. **Download Form 26AS first** - It shows all your reported income. Your ITR must match this!

2. **Keep digital copies** - Scan everything. You might need them for 7 years.

3. **Don't have Form 16?** No worries! You can still file using salary slips and Form 26AS.

4. **TDS mismatch?** Contact your employer/deductor immediately. They need to file a correction statement.

**Quick Check Before Filing:**
✅ Form 16 received?
✅ Form 26AS matches your income?
✅ All investment proofs ready?
✅ Bank account linked to PAN?
✅ Aadhaar linked to PAN?

Got all these? You're ready to file! Need help with the actual filing process? Just ask! 🚀""",
            
            "filing_deadline": """Tax filing deadlines:
- **Individuals (non-audit):** July 31st
- **Audit cases:** October 31st
- **Revised return:** December 31st
- **Belated return:** Up to December 31st (with penalty)

Missing deadline? File belated return with ₹5,000 penalty (₹1,000 if income < ₹5 lakh).""",
            
            "section_80c": """Ah, Section 80C - the superhero of tax savings! Let me explain this properly.

**What is Section 80C?**

It's a provision that lets you reduce your taxable income by up to **₹1.5 lakh per year** by investing in specified instruments. Think of it as the government saying, "Save money, pay less tax!"

**⚠️ Important Note:** These deductions are **only available in the Old Tax Regime**. If you've opted for the New Tax Regime, you can't claim these.

**Where Can You Invest for 80C Benefits?**

Let me break down your options:

**1. Government-Backed Savings:**
- **Public Provident Fund (PPF)** - 7.1% interest, 15-year lock-in, completely tax-free returns
- **Sukanya Samriddhi Yojana** - For girl child, 8% interest, runs till she turns 21
- **National Savings Certificate (NSC)** - 5-year term, 7-7.7% interest
- **Senior Citizens Savings Scheme** - Only for 60+ age, 8% interest

**2. Employee Contributions:**
- **EPF (Employee Provident Fund)** - Auto-deducted from salary
- **Voluntary Provident Fund (VPF)** - Extra voluntary contribution to EPF
- **NPS (Tier 1)** - National Pension System, also gets additional ₹50k under 80CCD(1B)

**3. Insurance:**
- **Life Insurance Premium** - For self, spouse, children
  - Only premium amount counts, not the sum assured
  - Maximum premium should be ≤10% of sum assured (policies after 2012)

**4. Market-Linked Investments:**
- **ELSS Mutual Funds** - Equity Linked Savings Scheme
  - Only 3-year lock-in (shortest among 80C!)
  - Potential for 10-15% returns
  - ₹500 minimum investment

**5. Fixed Deposits:**
- **5-Year Tax Saving FD** - With banks/post office
  - ~7% interest, but interest is taxable
  - Premature withdrawal not allowed

**6. Home Loan:**
- **Principal Repayment** - The EMI principal part (not interest!)
  - Interest goes under Section 24 (different limit)

**7. Education:**
- **Tuition Fees** - For up to 2 children
  - Only tuition fees, not development charges
  - School, college, university all covered

**💡 Smart Tips:**

**Best Combinations for Different People:**

**For Beginners:**
- ELSS: ₹50,000 (shortest lock-in, good returns)
- PPF: ₹50,000 (safe, tax-free)
- EPF: ₹50,000 (auto contribution)

**For Risk-Takers:**
- ELSS: ₹1,00,000 (higher returns)
- NPS: ₹50,000 (extra ₹50k deduction separately!)

**For Ultra-Safe Investors:**
- PPF: ₹1,50,000 (all in one place, completely safe)

**Common Mistakes to Avoid:**

❌ Investing just for tax saving without checking returns
❌ Putting all money in December rush - spread throughout the year
❌ Not considering lock-in periods
❌ Forgetting that LIC premiums >10% of sum assured don't qualify
❌ Claiming for development fees or transport fees (not eligible!)

**Quick Example:**

Your taxable income: ₹10 lakh
You invest: ₹1.5 lakh in 80C instruments
New taxable income: ₹8.5 lakh

**Tax saved:** ₹30,000 (at 20% slab) + ₹1,200 cess = **₹31,200!**

That's a solid return just on tax savings, plus whatever your investments earn! 🎯

Want recommendations on which 80C instruments suit you best? Just ask! 😊""",
            
            "old_vs_new": """This is THE million-dollar question (or should I say, tax-saving question)! Let me help you figure this out.

**First, let's understand what each regime actually means:**

**🆕 New Tax Regime:**
Think of this as the "keep it simple" option. Lower tax rates, but you give up almost all deductions.

**Pros:**
- **Lower tax slabs** - You start paying tax only after ₹3 lakh (vs ₹2.5 lakh in old)
- **Simple filing** - No need to collect investment proofs
- **Less paperwork** - Just declare income and you're done
- **Better for higher incomes** with no deductions

**Cons:**
- **No deductions allowed** (except employer NPS contribution - 80CCD(2))
- **No HRA exemption**
- **No standard deduction benefits** on investments
- **No LTA, no home loan benefits**

**📜 Old Tax Regime:**
The traditional system - higher tax rates but TONS of deductions to reduce your taxable income.

**Pros:**
- **All deductions available**: 80C, 80D, HRA, LTA, home loan, etc.
- **Can reduce taxable income significantly**
- **Better if you invest regularly**
- **Proven, well-understood system**

**Cons:**
- **Higher base tax rates**
- **More documentation needed**
- **Complex calculations**

**🧮 Now, Let's Do the Math:**

**Who Should Choose NEW Regime?**

✅ **You, if:**
1. Your income is ₹7-10 lakh with **no investments**
2. You live in a rented place (no HRA claim anyway)
3. You don't have home loan
4. You prefer simple filing
5. You don't invest in 80C instruments

**Example:** Salary ₹8 lakh, no investments
- **New regime tax:** ₹25,000 + cess = ₹26,000
- **Old regime tax:** ₹62,500 + cess = ₹65,000
**Winner: New Regime** (saves ₹39,000!)

**Who Should Choose OLD Regime?**

✅ **You, if:**
1. You have **home loan** (interest component)
2. You get **HRA** and live in rented house
3. You invest ₹1.5L+ annually (80C + 80D + NPS)
4. You claim **LTA** (Leave Travel Allowance)
5. Your income is **₹10 lakh+** with investments

**Example:** Salary ₹12 lakh
- Investments: ₹1.5L (80C) + ₹25k (80D) + ₹50k (NPS)
- HRA: ₹1L
- Home loan interest: ₹2L
**Total deductions: ₹4.25L**

Taxable income becomes: ₹7.75L
- **Old regime tax:** ₹75,500
- **New regime tax:** ₹1,30,000
**Winner: Old Regime** (saves ₹54,500!)

**🎯 Quick Decision Tree:**

**Step 1:** Calculate your deductions
- 80C investments: ₹____
- HRA exemption: ₹____
- Home loan interest: ₹____
- Health insurance (80D): ₹____
- NPS additional: ₹____
**Total: ₹____**

**Step 2:** Compare
- If total deductions < ₹2.5 lakh → **Choose New Regime**
- If total deductions > ₹2.5 lakh → **Choose Old Regime**

**💡 Pro Tips:**

1. **You can switch every year!** Not permanent. Choose based on that year's situation.

2. **For business/profession**: Old regime might be better due to additional deductions.

3. **Use an online calculator**: Input your numbers and compare. Don't guess!

4. **Consider your age**: Senior citizens get higher 80D deductions in old regime.

5. **Think future**: If you're planning home loan or big investments, old regime makes sense.

**Common Scenarios:**

**Fresh Graduate (₹6L salary, no investments):**
→ **New Regime** (₹15,600 vs ₹33,800 - saves ₹18,200!)

**Mid-career (₹10L, ₹1.5L investments, HRA):**
→ **Old Regime** (more deductions = more savings)

**Senior executive (₹20L+, active investor):**
→ **Old Regime** (higher deductions offset higher rates)

**Still confused?** Share your:
- Annual income
- Investments/deductions
- HRA/rent situation
- Home loan status

I'll tell you which regime saves you more! 🎯""",
            
            "gst_filing": """GST Return Filing:
- **GSTR-1:** Monthly/Quarterly sales return
- **GSTR-3B:** Monthly summary return
- **GSTR-9:** Annual return

Login to GST portal, use valid digital signature, file before due date. Late fees: ₹50/day (₹20 for nil returns) per act.""",
            
            "tds": """Let me explain TDS - it's actually simpler than it sounds!

**What is TDS (Tax Deducted at Source)?**

Think of TDS as "advance tax payment" that happens automatically. Instead of you paying all your taxes at year-end, someone else (employer, bank, etc.) deducts a portion when they pay you and deposits it to the government on your behalf.

**Why TDS Exists:**
- Ensures regular tax collection throughout the year
- Prevents tax evasion
- Makes year-end filing easier (tax already paid!)

**How TDS Works - A Simple Example:**

Let's say your salary is ₹50,000/month.
1. Your employer calculates your annual tax liability: ₹50,000
2. They deduct ₹4,167 every month from your salary
3. They deposit this to the government with your PAN
4. You receive ₹45,833 in hand
5. At year-end, you file ITR and get refund if excess was deducted!

**Common TDS Rates You'll Encounter:**

**On Salary:**
- Deducted as per applicable tax slab
- Employer considers your investments for deduction
- Form 16 issued annually

**On Interest Income:**
- **Bank FD/Savings:** 10% TDS if interest > ₹40,000/year (₹50,000 for seniors)
- Can submit Form 15G/15H if no tax liability (to avoid TDS)

**On Professional/Freelance Fees:**
- **Section 194J:** 10% TDS on fees > ₹30,000
- Applies to: consultants, doctors, lawyers, technical services

**On Rent:**
- **For Individuals:** 5% if rent > ₹50,000/month (new rule from April 2024)
- **For Companies:** 10% on rent

**On Contract Payments:**
- 1-2% depending on type
- Applicable to contractors, transporters

**On Winning from Lottery/Game Shows:**
- 30% TDS (highest rate!)
- Applied on any winning > ₹10,000

**📋 Important Documents:**

**Form 16:** Your TDS certificate from employer
- Part A: TDS details
- Part B: Salary breakup & deductions
- Needed for ITR filing!

**Form 26AS:** Your complete tax credit statement
- Shows ALL TDS deducted across sources
- Updated quarterly
- Download from income tax portal

**Form 16A:** TDS certificate for non-salary income
- From bank (interest), tenant (rent), client (professional fees)

**🔍 How to Check Your TDS Credits:**

1. Visit: incometax.gov.in
2. Login with PAN
3. Go to "View Form 26AS"
4. Select financial year
5. Verify all TDS entries

**What to Do if TDS is Deducted:**

**Scenario 1: Excess TDS Deducted**
Example: Your tax liability is ₹40,000 but TDS deducted is ₹60,000
→ File ITR and claim ₹20,000 refund!

**Scenario 2: Insufficient TDS**
Tax liability: ₹60,000, TDS: ₹40,000
→ Pay remaining ₹20,000 as self-assessment tax before filing ITR

**Scenario 3: TDS Deducted but Wrong PAN**
→ Contact the deductor immediately to file a correction statement

**💡 Pro Tips:**

**1. Submit Investment Proof to Employer Early:**
If you submit PPF, insurance proofs to employer, they'll deduct less TDS throughout the year (more money in hand!).

**2. Form 15G/15H:**
If your total income is below taxable limit:
- Form 15G (below 60 years)
- Form 15H (60+ years)
Submit to bank to prevent TDS on interest.

**3. Regular Tracking:**
Check Form 26AS every quarter. Ensures:
- All TDS is credited to your PAN
- No discrepancies at filing time
- No last-minute surprises!

**4. TDS Mismatch?**
If Form 16 shows ₹50,000 TDS but 26AS shows ₹45,000:
→ Employer hasn't deposited or wrong PAN quoted
→ Contact employer IMMEDIATELY (they must file correction)

**5. Lower Deduction Certificate:**
If you're in lower tax bracket or no tax liability, apply for Form 13 (lower/nil TDS certificate) from Income Tax office.

**Common Questions:**

**Q: Can TDS be refunded?**
Yes! If excess TDS deducted, file ITR and claim refund (takes 4-8 weeks).

**Q: What if deductor doesn't give me TDS certificate?**
Check Form 26AS. If TDS is credited there, you can file ITR. Also report deductor to TDS cell.

**Q: Is TDS my final tax?**
No! TDS is just advance payment. Final tax calculated when you file ITR. You might need to pay more or get refund.

**Quick Summary:**
- TDS = Tax paid in advance on your behalf
- Always check Form 26AS
- Claim refund if excess TDS
- Pay balance if TDS insufficient

Need help with TDS on specific income type? Just ask! 😊""",
            
            "refund_status": """Check refund status:
1. Visit incometax.gov.in
2. Go to 'Refund Status'
3. Enter PAN and Assessment Year
4. View status

Refund typically takes 4-8 weeks. Credited directly to bank account mentioned in ITR.""",
            
            "pan_card": """**Apply for PAN:**
- Visit NSDL/UTIITSL websites
- Fill Form 49A (Indian)/49AA (Foreign)
- Submit documents (ID, address, DOB proof)
- Pay ₹110 fee
- Receive PAN in 15 days

**Update PAN:** Use Form 49A for corrections via same portals.""",
            
            "advance_tax": """**Advance Tax:** Pay in installments if liability > ₹10,000
- June 15: 15%
- Sept 15: 45%
- Dec 15: 75%
- March 15: 100%

Calculate using Form 26AS projection. Interest charged at 1% per month for late payment."""
        }
    },
    
    "mutual_funds": {
        "keywords": ["mutual fund", "sip", "nav", "equity", "debt", "hybrid", "investment", "redemption", "elss", "fund", "portfolio", "lumpsum", "kyc"],
        "responses": {
            "what_are_mf": """Great question! Let me break down mutual funds in the simplest way possible.

**What Exactly Are Mutual Funds?**

Imagine you and 99 friends want to invest in stocks, but:
- None of you knows which stocks to buy
- You each have only ₹1,000 (not enough to diversify)
- You don't have time to track the market daily

So you all pool your money (₹1,00,000 total) and hire an expert fund manager to invest on your behalf. That's essentially a mutual fund!

**The Simple Definition:**
A mutual fund is a pool of money collected from many investors, invested by professionals in stocks, bonds, or other securities.

**How Do They Actually Work?**

Let me walk you through the journey:

**Step 1: You Invest**
You buy "units" of a mutual fund. Think of units like shares.
- If NAV (price per unit) = ₹100
- You invest ₹10,000
- You get 100 units

**Step 2: Fund Manager Invests**
The fund manager (experienced professional) uses everyone's pooled money to:
- Buy multiple stocks/bonds (diversification!)
- Research companies
- Make buying/selling decisions daily
- Rebalance the portfolio

**Step 3: You Earn Returns**
When the investments grow:
- Your units' value increases (NAV goes up)
- Some funds also give dividends
- You can sell (redeem) units anytime (mostly!)

**Why Mutual Funds Are Awesome:**

**1. Professional Management:**
You don't need to be a stock market expert. Leave it to professionals who do this full-time!

**2. Diversification Made Easy:**
With just ₹500, you can own a piece of 50+ companies. Imagine buying 50 stocks individually - expensive and complicated!

**3. Affordability:**
Start with as low as ₹500 (through SIP). No huge capital needed.

**4. Liquidity:**
Most funds let you withdraw money anytime (except ELSS - 3 year lock-in).

**5. Transparency:**
- NAV updated daily
- Portfolio disclosed regularly
- Regulated by SEBI (safe!)

**6. Tax Benefits:**
- ELSS funds offer Section 80C deductions
- Long-term equity gains taxed at only 12.5%

**Real-Life Example:**

**Scenario:** Rahul invests ₹5,000/month via SIP in an equity mutual fund for 10 years.

**Without Mutual Fund:**
- He'd need to research 30+ stocks
- Buy/sell regularly
- Track quarterly results
- Rebalance portfolio
**Time needed:** 10+ hours/month!

**With Mutual Fund:**
- Set up SIP once (takes 10 minutes)
- Fund manager does everything
- Rahul just monitors once a month
**Time needed:** 15 minutes/month!

**Result:** After 10 years at 12% returns:
- Total invested: ₹6,00,000
- Final value: ₹11,61,695
**Profit: ₹5,61,695!** 🎉

**How Mutual Funds Make Money:**

**1. NAV Appreciation (Growth Option):**
- You buy at NAV ₹100
- After 3 years, NAV becomes ₹150
- You sell and make ₹50 profit per unit

**2. Dividends (Dividend Option):**
- Fund declares dividend from profits
- You receive periodic payouts
- NAV reduces by dividend amount

**The Mutual Fund Ecosystem:**

**Key Players:**
1. **You (Investor)** - The money provider
2. **AMC (Asset Management Company)** - The fund house (e.g., HDFC MF, ICICI Prudential)
3. **Fund Manager** - The expert who invests
4. **Custodian** - Safeguards your securities
5. **Registrar** - Maintains your account records
6. **SEBI** - The regulator ensuring fair play

**Types of Returns:**

**Absolute Returns:** Simple profit percentage
- Invested ₹1,00,000 → Became ₹1,30,000
- Absolute return = 30%

**Annualized Returns:** Returns per year (better for comparing)
- 30% in 2 years = ~14% per year

**CAGR (Compounded Annual Growth Rate):** Most accurate
- Shows steady growth rate considering compounding

**Common Myths Busted:**

❌ **"Mutual funds guarantee returns"**
✅ No guarantees! Returns depend on market performance.

❌ **"Only for rich people"**
✅ Start with just ₹500/month via SIP!

❌ **"Too risky, might lose all money"**
✅ Diversification reduces risk. Long-term investing has historically given positive returns.

❌ **"I need Demat account"**
✅ Not needed! Direct investment with AMC or through platforms.

❌ **"Can't withdraw when I need"**
✅ Most funds allow redemption in 3-7 days (except ELSS).

**Fees You Should Know:**

**1. Expense Ratio:**
Annual fee charged by AMC (usually 0.5-2.5%)
- Equity funds: 1.5-2.5%
- Debt funds: 0.5-1%
Lower is better!

**2. Exit Load:**
Penalty for redeeming too early (usually 1% if < 1 year)

**3. Transaction Charges:**
₹100 for investments ≥ ₹10,000 (one-time)

**Quick Comparison:**

**Mutual Funds vs Direct Stocks:**
- MF: Professionally managed, diversified, easier
- Stocks: You manage, concentrated, needs expertise

**Mutual Funds vs Fixed Deposits:**
- MF: Higher returns (10-12%), market-linked risk
- FD: Fixed returns (6-7%), capital safe

**Mutual Funds vs Real Estate:**
- MF: Highly liquid, start small, diversified
- Real Estate: Illiquid, needs large capital, location-dependent

**Getting Started is Easy:**

1. Complete KYC (one-time, online/offline)
2. Choose a fund (I can help!)
3. Invest lumpsum or start SIP
4. Monitor quarterly (don't obsess daily!)

**Bottom Line:**

Think of mutual funds as:
- Your personal finance team
- Working 24/7 to grow your money
- While you focus on your career/life

Perfect for beginners and experts alike!

Want to know which type of mutual fund suits you? Ask away! 😊""",
            
            "types_of_mf": """**Types of Mutual Funds:**

**Equity Funds:** Invest in stocks
- Large Cap (stable companies)
- Mid Cap (growing companies)
- Small Cap (high risk, high return)
- Multi Cap (diversified)

**Debt Funds:** Invest in bonds/fixed income
- Liquid funds, Gilt funds, Corporate bonds
- Lower risk than equity

**Hybrid Funds:** Mix of equity & debt
- Balanced risk-return profile

**ELSS:** Tax-saving equity funds (3-year lock-in)""",
            
            "start_sip": """**Starting a SIP:**
1. Complete KYC (Aadhaar, PAN, photo)
2. Choose fund based on goal & risk appetite
3. Select SIP amount (min ₹500-1000)
4. Choose frequency (monthly/quarterly)
5. Set up auto-debit mandate
6. Submit application online/offline

**Benefits:** Rupee cost averaging, disciplined investing, power of compounding.""",
            
            "nav": """**NAV (Net Asset Value):**
Price of one unit of mutual fund.

**Formula:** NAV = (Total Assets - Liabilities) / Total Units

Updated daily at end of trading day. Check NAV on:
- Fund house website
- AMFI website
- Investment apps

**Note:** NAV doesn't indicate fund quality, check returns & portfolio.""",
            
            "tax_implications": """**Mutual Fund Taxation:**

**Equity Funds:**
- Short-term (<1 year): 20% tax
- Long-term (>1 year): 12.5% on gains above ₹1.25 lakh/year

**Debt Funds:**
- Taxed as per your income slab (both short & long term)

**ELSS:** Gains above ₹1.25 lakh taxed at 12.5% after 3 years
**Dividend:** Taxed as per your slab

STP/SWP taxation applies on each redemption.""",
            
            "redemption": """**Redeem Mutual Funds:**
1. Login to fund house/broker portal
2. Select 'Redeem' option
3. Choose units or amount
4. Verify bank details
5. Submit request

**Processing:** Amount credited in 3-7 working days
**Exit Load:** May apply if redeemed before specified period (usually 1 year)

**Switch:** Move between funds of same house without redemption.""",
            
            "choosing_fund": """**Choose Mutual Fund based on:**
1. **Investment Goal:** Retirement, education, wealth creation
2. **Time Horizon:** Short-term (debt), Long-term (equity)
3. **Risk Appetite:** Low (debt), Moderate (hybrid), High (equity)
4. **Fund Performance:** Compare 3-5 year returns
5. **Expense Ratio:** Lower is better (<1% for equity)
6. **Fund Manager Track Record**
7. **AUM (Assets Under Management):** Higher indicates trust

Diversify across 4-6 funds maximum.""",
            
            "risks": """**Mutual Fund Risks:**
- **Market Risk:** NAV fluctuates with market
- **Credit Risk:** Default by bond issuers (debt funds)
- **Liquidity Risk:** Difficulty in redemption
- **Concentration Risk:** Over-exposure to few stocks
- **Interest Rate Risk:** Affects debt funds

**Mitigation:** Diversify, invest for long-term, review periodically, choose quality funds."""
        }
    },
    
    "insurance": {
        "keywords": ["insurance", "policy", "premium", "claim", "term", "health", "life", "vehicle", "coverage", "renewal", "sum assured", "mediclaim", "cashless"],
        "responses": {
            "types_of_insurance": """**Types of Insurance:**

**Life Insurance:**
- **Term:** Pure protection, high cover, low premium
- **Endowment:** Savings + protection
- **ULIP:** Market-linked returns
- **Whole Life:** Coverage till 100 years

**Health Insurance:**
- Individual/Family floater plans
- Critical illness cover
- Top-up/Super top-up plans

**Vehicle Insurance:**
- Third-party (mandatory)
- Comprehensive (own damage + third-party)""",
            
            "get_quote": """**Get Insurance Quote:**

**Online:**
1. Visit insurer website/aggregators
2. Enter age, coverage amount, term
3. Compare plans & premiums
4. Choose add-ons if needed

**Factors affecting premium:**
- Age, health condition, lifestyle
- Sum assured/coverage amount
- Policy term
- Smoking/drinking habits
- Pre-existing conditions""",
            
            "claim_filing": """**File Insurance Claim:**

**Health Insurance:**
1. **Cashless:** Show health card at network hospital
2. **Reimbursement:** Pay & submit bills with claim form
   - Discharge summary
   - Bills & prescriptions
   - Investigation reports
   - Pre-authorization form

**Life Insurance:**
- Death certificate
- Claim form
- Policy document
- Nominee ID proof

**Timeline:** Intimate within 24-48 hours, submit docs within 15 days.""",
            
            "claim_status": """**Check Claim Status:**
1. Visit insurer portal/app
2. Login with policy number
3. Go to 'Track Claim'
4. Enter claim ID

**Or:**
- Call customer care
- SMS to insurer's number
- Email with claim details

**Settlement time:** 30 days for health, 60 days for life (regulatory timeline).""",
            
            "renewal": """**Renew Insurance Policy:**
- Renew before expiry to avoid coverage gap
- **Grace Period:** 30 days for health/life, 90 days for vehicle
- **Online:** Via insurer portal, payment gateway
- **Offline:** Through agent/branch

**Check before renewal:**
- Premium changes
- Coverage adequacy
- Add riders if needed
- Update nominee/address

**Tip:** Set auto-renewal to avoid lapse.""",
            
            "coverage_details": """**What's Covered:**

**Health Insurance:**
- Hospitalization expenses
- Pre/post hospitalization (30-60 days)
- Day care procedures
- Ambulance charges
- Room rent (as per plan)

**Term Insurance:**
- Death benefit to nominee
- Optional riders: accidental death, critical illness

**Vehicle Insurance:**
- Comprehensive: Own damage + third-party liability
- Add-ons: Zero depreciation, engine protection, NCB protection""",
            
            "exclusions": """**Common Exclusions:**

**Health:**
- Pre-existing diseases (2-4 year wait)
- Cosmetic surgery
- Self-inflicted injuries
- War/nuclear risks

**Life:**
- Suicide (first year)
- Death due to illegal activities
- Non-disclosure of material facts

**Vehicle:**
- Drunk driving
- No valid license
- Wear & tear

**Always read policy document carefully!**"""
        }
    },
    
    "government_schemes": {
        "keywords": ["scheme", "government", "pmay", "pm kisan", "atal pension", "subsidy", "welfare", "yojana", "pension", "ayushman", "mudra", "jan dhan", "eligibility"],
        "responses": {
            "popular_schemes": """**Popular Government Schemes:**

**PMAY (Housing):** Interest subsidy on home loans
**PM-KISAN:** ₹6,000/year to farmers (3 installments)
**Atal Pension Yojana:** Guaranteed pension ₹1,000-5,000/month
**Ayushman Bharat:** Health cover up to ₹5 lakh
**MUDRA Loan:** Business loans up to ₹10 lakh
**Jan Dhan Yojana:** Zero-balance bank accounts
**Sukanya Samriddhi:** Savings for girl child
**PM Ujjwala:** Free LPG connections
**PM Fasal Bima:** Crop insurance""",
            
            "pmay_details": """**PMAY (Pradhan Mantri Awas Yojana):**

**Eligibility:**
- No pucca house in family's name
- Annual income: ₹3-18 lakh (MIG), <₹3 lakh (EWS/LIG)
- Not availed central govt housing benefits

**Benefits:**
- Interest subsidy 3-6.5% on home loans
- Credit-linked subsidy up to ₹2.67 lakh

**Apply:** Through bank/HFC website with Aadhaar, income proof, property documents.""",
            
            "atal_pension": """**Atal Pension Yojana (APY):**

**Eligibility:** 18-40 years, Indian citizen, savings bank account

**Benefits:** Guaranteed pension ₹1,000-5,000/month after 60 years

**Contribution:** ₹42-1,454/month based on entry age & pension amount

**Tax Benefit:** Deduction under Section 80CCD (up to ₹1.5 lakh)

**Apply:** Through bank with Aadhaar & auto-debit mandate.""",
            
            "pm_kisan": """**PM-KISAN:**

**Eligibility:** All landholding farmers

**Benefits:** ₹6,000/year in 3 installments of ₹2,000

**Exclusions:**
- Govt employees
- Income taxpayers
- Professionals

**Apply:** Visit pmkisan.gov.in, Aadhaar mandatory

**Check Status:** With Aadhaar/mobile number on portal.""",
            
            "ayushman_bharat": """**Ayushman Bharat (PM-JAY):**

**Coverage:** ₹5 lakh/family/year health insurance

**Eligibility:** Based on SECC 2011 data (deprived categories)

**Benefits:**
- Cashless treatment at empaneled hospitals
- Covers 1,500+ procedures
- No premium payment

**Check Eligibility:** Visit pmjay.gov.in or call 14555

**Card:** Download from website or get at hospital.""",
            
            "mudra_loan": """**MUDRA Loan:**

**Categories:**
- **Shishu:** Up to ₹50,000
- **Kishore:** ₹50,001 to ₹5 lakh
- **Tarun:** ₹5,00,001 to ₹10 lakh

**Eligibility:** Entrepreneurs, small businesses, startups

**No Collateral Required**

**Apply:** Through banks/NBFCs with business plan, ID proof, business registration.""",
            
            "scheme_status": """**Check Scheme Application Status:**

**Online:**
1. Visit respective scheme website
2. Click 'Track Application'
3. Enter application/reference number
4. View status

**Common Portals:**
- PM-KISAN: pmkisan.gov.in
- PMAY: pmaymis.gov.in
- Ayushman Bharat: pmjay.gov.in

**Helplines:**
- PM-KISAN: 155261 / 011-23381092
- PMAY: 1800-11-6163
- PM-JAY: 14555""",
            
            "required_documents": """**Common Documents for Schemes:**

**Mandatory:**
- Aadhaar card
- PAN card (if applicable)
- Bank account details
- Mobile number

**Additional (scheme-specific):**
- Income certificate
- Caste certificate
- Domicile certificate
- Land records (for farmer schemes)
- Business registration (for MUDRA)
- Property documents (for PMAY)
- Ration card (for welfare schemes)"""
        }
    }
}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat_started' not in st.session_state:
    st.session_state.chat_started = False

def get_category_from_query(query):
    """Determine the category of the query"""
    query_lower = query.lower()
    
    for category, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"]:
            if keyword in query_lower:
                return category
    return None

def get_response(query):
    """Generate response based on the query"""
    category = get_category_from_query(query)
    
    if not category:
        return """Hmm, I'm not quite sure what you're asking about. I can help you with:
        
🏦 **Taxation** - Income tax, GST, TDS, deductions, filing
💰 **Mutual Funds** - SIP, NAV, equity/debt funds, investments
🛡️ **Insurance** - Term, health, life, vehicle insurance, claims
🏛️ **Government Schemes** - PMAY, PM-KISAN, Atal Pension, Ayushman Bharat

Try asking something like:
- "How do I calculate my income tax?"
- "What are mutual funds?"
- "How do I file an insurance claim?"
- "Tell me about PM-KISAN scheme" """
    
    query_lower = query.lower()
    responses = KNOWLEDGE_BASE[category]["responses"]
    
    # More specific pattern matching for better accuracy
    if category == "taxation":
        if "80c" in query_lower or ("section" in query_lower and "deduction" in query_lower):
            return responses["section_80c"]
        elif "tds" in query_lower:
            return responses["tds"]
        elif ("old" in query_lower and "new" in query_lower) or "regime" in query_lower or "which" in query_lower:
            return responses["old_vs_new"]
        elif "gst" in query_lower:
            return responses["gst_filing"]
        elif "pan" in query_lower:
            return responses["pan_card"]
        elif "advance" in query_lower and "tax" in query_lower:
            return responses["advance_tax"]
        elif any(word in query_lower for word in ["refund", "status", "track", "check"]) and ("refund" in query_lower or "26as" in query_lower):
            return responses["refund_status"]
        elif any(word in query_lower for word in ["deadline", "last date", "due date", "when"]):
            return responses["filing_deadline"]
        elif any(word in query_lower for word in ["document", "paper", "need", "require"]) and any(word in query_lower for word in ["file", "filing", "itr"]):
            return responses["filing_documents"]
        elif any(word in query_lower for word in ["calculate", "computation", "slab", "rate", "how much"]):
            return responses["calculate_tax"]
        elif any(word in query_lower for word in ["file", "filing", "return", "itr"]):
            return responses["filing_documents"]
        else:
            # Better default for general taxation queries
            if any(word in query_lower for word in ["tax", "taxation", "income tax"]):
                return responses["calculate_tax"]
            return responses["calculate_tax"]
    
    elif category == "mutual_funds":
        if any(word in query_lower for word in ["what", "meaning", "define", "explain"]) and "mutual" in query_lower:
            return responses["what_are_mf"]
        elif any(word in query_lower for word in ["type", "kind", "category", "equity", "debt", "hybrid"]):
            return responses["types_of_mf"]
        elif "sip" in query_lower or "systematic" in query_lower:
            return responses["start_sip"]
        elif "nav" in query_lower:
            return responses["nav"]
        elif "tax" in query_lower:
            return responses["tax_implications"]
        elif any(word in query_lower for word in ["redeem", "withdraw", "exit", "switch"]):
            return responses["redemption"]
        elif any(word in query_lower for word in ["choose", "select", "best", "good"]):
            return responses["choosing_fund"]
        elif "risk" in query_lower:
            return responses["risks"]
        else:
            return responses["what_are_mf"]
    
    elif category == "insurance":
        if any(word in query_lower for word in ["type", "kind", "available"]):
            return responses["types_of_insurance"]
        elif any(word in query_lower for word in ["quote", "price", "cost", "premium"]) and "calculate" not in query_lower:
            return responses["get_quote"]
        elif any(word in query_lower for word in ["file", "filing", "submit"]) and "claim" in query_lower:
            return responses["claim_filing"]
        elif "status" in query_lower or "track" in query_lower:
            return responses["claim_status"]
        elif "renew" in query_lower:
            return responses["renewal"]
        elif any(word in query_lower for word in ["cover", "include", "benefit"]):
            return responses["coverage_details"]
        elif any(word in query_lower for word in ["exclusion", "not cover", "exclude"]):
            return responses["exclusions"]
        else:
            return responses["types_of_insurance"]
    
    elif category == "government_schemes":
        if "pmay" in query_lower or "housing" in query_lower:
            return responses["pmay_details"]
        elif "atal" in query_lower or "pension" in query_lower:
            return responses["atal_pension"]
        elif "kisan" in query_lower or "farmer" in query_lower:
            return responses["pm_kisan"]
        elif "ayushman" in query_lower or "health" in query_lower:
            return responses["ayushman_bharat"]
        elif "mudra" in query_lower or "loan" in query_lower:
            return responses["mudra_loan"]
        elif "status" in query_lower or "track" in query_lower:
            return responses["scheme_status"]
        elif "document" in query_lower:
            return responses["required_documents"]
        else:
            return responses["popular_schemes"]
    
    return "I can help with that! Could you be more specific about what you'd like to know?"

# Streamlit UI
st.set_page_config(
    page_title="BrokeGPT - Financial Assistant",
    page_icon="💸",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .tagline {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .category-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">💸 BrokeGPT</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Your go-to bot for decoding taxes, mutual funds, insurance & government schemes</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📚 Quick Topics")
    
    if st.button("🏦 Taxation"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about taxation"})
        response = get_response("Tell me about taxation")
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_started = True
        st.rerun()
    
    if st.button("💰 Mutual Funds"):
        st.session_state.messages.append({"role": "user", "content": "What are mutual funds?"})
        response = get_response("What are mutual funds?")
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_started = True
        st.rerun()
    
    if st.button("🛡️ Insurance"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about insurance"})
        response = get_response("Tell me about insurance")
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_started = True
        st.rerun()
    
    if st.button("🏛️ Government Schemes"):
        st.session_state.messages.append({"role": "user", "content": "What government schemes are available?"})
        response = get_response("What government schemes are available?")
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_started = True
        st.rerun()
    
    st.divider()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_started = False
        st.rerun()
    
    st.divider()
    st.markdown("### 💡 Example Questions")
    st.markdown("""
    - How do I file ITR?
    - What is Section 80C?
    - How to start a SIP?
    - Types of insurance
    - PM-KISAN eligibility
    """)

# Welcome message
if not st.session_state.chat_started and len(st.session_state.messages) == 0:
    welcome_msg = """Hey there! Welcome to **BrokeGPT** — your go-to bot for decoding taxes without the tears, making mutual funds less mysterious, insurance clearer than your 2 a.m. thoughts, and government schemes simpler than ordering coffee on credit. 

Ask me anything — let's untangle your money mess, one broke insight at a time. 💸

**What can I help you with today?**
- 🏦 Income Tax & GST queries
- 💰 Mutual Fund investments
- 🛡️ Insurance policies & claims
- 🏛️ Government schemes & subsidies"""
    
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    st.session_state.chat_started = True

# Chat interface
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me about taxes, mutual funds, insurance, or government schemes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Let me think about that... 🤔"):
            import time
            time.sleep(0.8)  # Short pause for natural feel
            response = get_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>⚠️ <b>Disclaimer:</b> This chatbot provides general information only. Please consult a qualified financial advisor or tax professional for personalized advice.</p>
    <p>Made with ❤️ for the financially confused | Not financial advice, just financial vibes</p>
</div>
""", unsafe_allow_html=True)