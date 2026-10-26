# What Drives AI Adoption in UK Small and Medium Businesses?

**Independent personal research project, unpaid and non-commercial, done in my own time using public data only. Not affiliated with, funded by or representing my employer or any organisation. Not advice.**

---

## Abstract

This study examines drivers of artificial intelligence (AI) adoption among UK small and medium-sized enterprises (SMEs) using data from the Office for National Statistics Business Insights and Conditions Survey (BICS) Wave 105 (March 2024). Analysis of 396 firm-technology observations reveals that 16.3% of micro firms (0-9 employees), 17.3% of small firms (10-49 employees), 14.7% of medium firms (50-249 employees), and 15.2% of large firms (250+ employees) report current AI use. Contrary to conventional wisdom, firm size shows no significant correlation with AI adoption (ρ = 0.095, p = 0.30). The primary reported purpose for AI use is improving business operations (35.6%), whilst the top substantive barrier is difficulty identifying business use cases (6.3%), closely followed by lack of expertise (6.8%) and cost (6.8%). These findings suggest that AI adoption among UK SMEs is driven more by practical operational needs and constrained by knowledge gaps than by firm resources alone.

## 1. Introduction

Artificial intelligence adoption in small and medium businesses has become a policy priority in the UK, with government initiatives targeting productivity growth through digital transformation. However, empirical evidence on what drives or inhibits AI uptake among smaller firms remains limited. This study uses nationally representative survey data to examine three questions: (1) Does firm size predict AI adoption? (2) What purposes drive AI use? (3) What barriers prevent adoption?

### Research Hypotheses
- H1: Larger firms have higher AI adoption rates than smaller firms
- H2: Lack of expertise is a more significant barrier than cost
- H3: Operational efficiency improvement is the primary driver of AI adoption

## 2. Data and Method

### Data Source
Data come from the ONS Business Insights and Conditions Survey (BICS) Wave 105, conducted 18-31 March 2024. BICS is a fortnightly survey of UK businesses weighted by count to be nationally representative. The survey includes questions on current AI technology use, purposes, adoption methods, planned adoption, and barriers (ONS, 2024).

This analysis uses:
- Current AI use by technology and firm size (396 observations)
- AI purposes among adopters (232 observations)
- Barriers to adoption (553 observations)
- Adoption methods (207 observations)

All data are licensed under the Open Government Licence v3.0 and downloaded on 26 October 2026 from the ONS website.

### Method
Descriptive statistics summarise AI adoption rates by firm size band (micro: 0-9 employees; small: 10-49; medium: 50-249; large: 250+). Spearman rank correlation tests the relationship between firm size and adoption rates. Barriers and purposes are aggregated across firm categories to identify top factors.

## 3. Results

### 3.1 AI Adoption by Firm Size
Mean AI adoption rates by size band show limited variation:
- Micro (0-9 employees): 16.3%
- Small (10-49 employees): 17.3%
- Medium (50-249 employees): 14.7%
- Large (250+ employees): 15.2%

Spearman correlation between firm size (coded 1-4) and AI adoption rate is 0.095 (p = 0.30), indicating no significant relationship. **H1 is not supported**: larger firm size does not predict higher AI adoption in this sample.

### 3.2 Purposes for AI Use
Among businesses currently using AI, the top reported purposes are:
1. Improve business operations: 35.6%
2. Provide or personalise products/services to customers: 19.2%
3. Develop a new product or service: 15.5%

**H3 is supported**: operational efficiency improvement is the primary stated driver of AI adoption.

### 3.3 Barriers to AI Adoption
Excluding meta-categories ("not attempted" and "not prevented"), the top substantive barriers are:
1. Difficulty identifying business use cases: 6.3%
2. Level of expertise in AI: 6.8%
3. Cost: 6.8%

Notably, 40.3% of businesses report they have not been prevented or delayed in AI adoption, and 35.6% report they have not attempted to use AI. Among those facing barriers, expertise and use-case identification are as prominent as cost. **H2 is partially supported**: expertise is a top barrier, but it ranks alongside cost rather than substantially exceeding it.

### 3.4 Adoption Methods
Among AI adopters who reported methods, the most common approaches are:
- Developed in-house (reported across multiple categories)
- Outsourced to external providers
- Purchase of external software/ready-to-use solutions

This suggests a mix of build and buy strategies, with no single dominant path.

## 4. Discussion

### Key Findings
This analysis yields three main findings. First, AI adoption rates among UK businesses show little variation by firm size, contradicting the common assumption that larger firms lead in technology uptake. Adoption rates cluster between 14.7% and 17.3% across all size bands. This suggests that AI technologies—particularly text generation using large language models, the most widely reported type—may have lower barriers to entry than previous waves of IT.

Second, businesses adopt AI primarily to improve operations, not to develop new products or enter new markets. This finding aligns with incremental innovation models: firms seek productivity gains from existing processes rather than radical transformation.

Third, the primary barriers to adoption are knowledge-related—difficulty identifying use cases and lack of expertise—rather than financial. Only 6.8% of businesses report cost as a barrier. This implies that AI adoption may be constrained more by organisational learning capacity than by capital availability.

### Limitations
Several limitations apply. First, this is cross-sectional data from a single survey wave, precluding causal inference. Second, the survey relies on self-reported AI use, which may be subject to interpretation: respondents may have differing understandings of what constitutes "AI". Third, adoption rates are aggregated across diverse industries, masking sector-specific patterns. Fourth, the analysis uses descriptive statistics and simple correlation; more sophisticated modelling (e.g. logistic regression with sector and regional controls) would strengthen inference. Fifth, the sample includes all firm sizes, but SMEs (under 250 employees) are the primary focus; results may not generalise to very large enterprises.

## 5. Conclusion

Using nationally representative ONS survey data, this study finds that AI adoption among UK businesses is not strongly predicted by firm size and is driven primarily by operational improvement needs. The main barriers are knowledge gaps—use-case identification and expertise—rather than cost. These findings suggest that policies to accelerate AI adoption should prioritise practical guidance and skills development over financial incentives alone. Future research should examine sector-specific adoption patterns and employ longitudinal data to trace adoption trajectories over time.

---

## References

Office for National Statistics (ONS). (2024). *Business Insights and Conditions Survey (BICS) Wave 105*. Retrieved 26 October 2026 from https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/businessinsightsandimpactontheukeconomy

All data licensed under the Open Government Licence v3.0: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

---

**Data and Code Availability**

All data processing and analysis code is available in this repository. The analysis is fully reproducible by running:
1. `python3 src/download_data.py` (downloads ONS data)
2. `python3 src/process_data.py` (processes raw data)
3. `python3 src/analyse.py` (generates results and figures)

Alternatively, run the Jupyter notebook: `notebooks/ai_adoption_analysis.ipynb`

Tests can be run with: `pytest tests/`

---

**Figures Calculated From:**
All percentages and statistics in this paper are calculated from ONS BICS Wave 105 data (18-31 March 2024) using the code in this repository. No figures are estimated, approximated, or taken from secondary sources.
