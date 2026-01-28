📊 S&P 500 vs. Case-Shiller Housing Index Analysis

<hr>

Overview:

<br>

This project explores the relationship between U.S. equity market performance and residential housing prices by analyzing historical data from the S&P 500 Index and the Case-Shiller U.S. National Home Price Index. Using time-series analysis techniques, the project examines correlations, rolling correlations, and potential lagged relationships between the two datasets.

The goal of this analysis is to identify patterns and associations, not to imply causation or make predictions.

<hr> 

Objectives:

<br>

- Analyze long-term trends in U.S. equity markets and housing prices

- Measure correlations between monthly market returns and housing price changes

- Examine how correlations vary over time using rolling windows

- Explore whether equity market movements tend to lead housing price changes

<hr>

Data Sources:

<br> 

- S&P 500 Index
  - Source: Kaggle “S&P 500 (^GSPC) Historical Data” by paveljurke
<br>

- Case-Shiller U.S. National Home Price Index
  - Source: Federal Reserve Economic Data (FRED), series CSUSHPINSA
  - Frequency: Monthly
<br> 

Time Range: 2000 – 2024

<hr>

Tools & Technologies:

<br>

- Python

- pandas

- NumPy

- matplotlib

- HTML and CSS

- Flask

<hr>

Methodology:

<br>

- Imported and cleaned monthly time-series data from both sources

- Converted date columns to datetime format and aligned datasets by date

- Visualized index levels to compare long-term trends

- Calculated monthly percentage changes to analyze market movement rather than absolute values

- Computed Pearson correlations between monthly returns

- Analyzed rolling correlations using a 12-month window

- Conducted exploratory lag analysis to assess whether equity market changes precede housing price changes

- Developed a Flask-based web interface to present and visualize analytical findings using HTML and CSS.

<hr>

Key Findings:

<br>

- The correlation between equity markets and housing prices varies over time

- Stronger correlations tend to appear during periods of economic stress

- Housing prices generally respond more slowly than equity markets

- No consistent or stable lead-lag relationship was observed across the entire time period

<hr> 

Limitations:

<br>

- Case-Shiller data is subject to reporting delays

- Analysis does not control for interest rates, inflation, or monetary policy

- Data represents national-level trends and does not reflect regional variation

- Correlation does not imply causation

<hr>

Conclusion:

<br>

This analysis demonstrates that while equity markets and housing prices are influenced by shared macroeconomic conditions, their relationship is not constant over time. The findings highlight the importance of temporal context when analyzing financial and economic data.

<hr>

Future Improvements:

<br>

- Incorporate interest rate and inflation data for multivariate analysis

- Analyze regional Case-Shiller indices

- Extend analysis with additional rolling window sizes

- Explore non-linear relationships using alternative correlation measures

<hr> 

Disclaimer:

<br>

This project is for educational purposes only and does not constitute financial or investment advice.
