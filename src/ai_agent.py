import pandas as pd

def get_ai_investment_brief(df, year):
    df_sorted = df.sort_values("Projected_Production", ascending=False)
    top = df_sorted.iloc[0]
    avg = df["Projected_Production"].mean()

    growth = top.get("Growth_Rate", 0)
    risk = top.get("Risk_Score", 0)

    return f"""
### 📊 Strategic Summary ({year})

**🏆 Best Region:** {top['Region']}  
**Projected Production:** {int(top['Projected_Production']):,} bbl  

📈 Growth Rate: {growth:.2f}  
⚠️ Risk Score: {risk:.2f}  

This region outperforms the average production of {int(avg):,} bbl.

### ✅ Recommendation:
This region shows {'strong growth' if growth > 0 else 'declining trend'} and 
{'low risk' if risk < df['Risk_Score'].mean() else 'higher volatility'}.

👉 Suggested Action: Prioritize investment and monitor trend sustainability.
"""


# 🔥 NEW: Conversational AI Agent
def chatbot_response(question, df, year):
    question = question.lower()

    df_sorted = df.sort_values("Projected_Production", ascending=False)
    top = df_sorted.iloc[0]
    bottom = df_sorted.iloc[-1]
    avg = int(df["Projected_Production"].mean())

    # -----------------------------
    # BEST REGION
    # -----------------------------
    if "best" in question or "highest" in question:
        return f"""
📍 **Best Region for {year}:**

👉 {top['Region']} leads with projected production of **{int(top['Projected_Production']):,} barrels**

📈 Growth: {top['Growth_Rate']:.2f}  
⚠️ Risk: {top['Risk_Score']:.2f}
"""

    # -----------------------------
    # WORST REGION
    # -----------------------------
    elif "worst" in question or "lowest" in question:
        return f"""
📍 **Lowest Performing Region:**

👉 {bottom['Region']} has projected production of **{int(bottom['Projected_Production']):,} barrels**

This may indicate weaker investment potential.
"""

    # -----------------------------
    # AVERAGE
    # -----------------------------
    elif "average" in question:
        return f"""
📊 **Average Production Across Regions:**

👉 {avg:,} barrels
"""

    # -----------------------------
    # GROWTH
    # -----------------------------
    elif "growth" in question:
        top_growth = df.sort_values("Growth_Rate", ascending=False).iloc[0]
        return f"""
📈 **Highest Growth Region:**

👉 {top_growth['Region']} with growth rate of **{top_growth['Growth_Rate']:.2f}**

This region is expanding rapidly.
"""

    # -----------------------------
    # RISK
    # -----------------------------
    elif "risk" in question:
        high_risk = df.sort_values("Risk_Score", ascending=False).iloc[0]
        return f"""
⚠️ **Highest Risk Region:**

👉 {high_risk['Region']} shows highest volatility (Risk Score: {high_risk['Risk_Score']:.2f})

This region may be less stable for investment.
"""

    # -----------------------------
    # WHY BEST
    # -----------------------------
    elif "why" in question:
        return f"""
🧠 **Why {top['Region']}?**

- Highest projected production  
- Growth rate: {top['Growth_Rate']:.2f}  
- Risk score: {top['Risk_Score']:.2f}  

👉 Strong combination of scale and trend.
"""

    # -----------------------------
    # DEFAULT
    # -----------------------------
    else:
        return """
💬 Try asking:

- "Which region is best?"
- "Which region has highest growth?"
- "Which region is risky?"
- "What is the average production?"
"""