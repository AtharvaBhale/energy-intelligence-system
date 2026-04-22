def get_ai_investment_brief(df, year):
    top = df.sort_values("Projected_Production", ascending=False).iloc[0]
    avg = df["Projected_Production"].mean()

    return f"""
### 📊 Strategic Summary ({year})

**Top Region:** {top['Region']}  
**Projected Production:** {int(top['Projected_Production']):,} bbl  

This region significantly outperforms the average production of {int(avg):,} bbl.

### ✅ Recommendation:
Prioritize investment in **{top['Region']}** due to strong projected output and competitive advantage.
"""