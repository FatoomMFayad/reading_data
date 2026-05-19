# 📊 Reading Data with Pandas

[![Pandas](https://img.shields.io/badge/library-pandas-orange.svg)](https://pandas.pydata.org/)
[![Community](https://img.shields.io/badge/Community-PSSAR-green.svg)](#)

A compact repository dedicated to reading, parsing, and filtering data files using Python and `pandas`.

---

## 🧠 Core Insights & Challenges

* **The Hurdle:** The most challenging part of this project is dealing with grouped data and applying filters on them efficiently.
* **The PSSAR Community:** Data reveals that the PSSAR research community is highly diverse. However, its financial ecosystem is centralized—**most funding relies heavily on the Machine Learning field.**

---

## 🚀 Key Code Snippets

### 1. Grouping & Filtering Challenges
Conquering complex aggregations by grouping data and isolating maximum values via index maximization:
```python
# Group by researcher and sum metrics
highest_citations_sum = merged_researchers_pub.groupby('researcher_id')['citations'].sum()

# Extract the index label of the maximum value
highest_citations_author_id = highest_citations_sum.idxmax()

# Filter active members and sort chronologically
first_active_joined = merged_researchers_pub[(merged_researchers_pub['is_active']== True)].sort_values('joined_year', ascending=True)

# Grab the name from the very first row (position 0)
first_active_name = first_active_joined.iloc[0]['name']
# Export to CSV without saving the default row index integers
merged_researchers_pub.to_csv('pssar_ml_insights.csv', index=False, encoding='utf-8-sig')