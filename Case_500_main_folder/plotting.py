import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


def generate_plot(data, title, filename):
    plt.figure(figsize=(10, 6))
    """
    Generates and saves specialized charts for the Flask interface.
    Handles both multi-column DataFrames and single-column Series.
    """

    if isinstance(data, pd.Series):
        # Single line case: Correlation
        plt.plot(data.index, data.values, label="Rolling Correlation", color="#5b27d6")
    else:
        # Multi-line case: Trends or Normalized
        for col in data.columns:
            if col == "SP500":
                plt.plot(data.index, data[col], label="S&P 500", 
                         color="#1fb44c", linewidth=2)
            elif col == "CaseShiller":
                plt.plot(data.index, data[col], label="Case-Shiller Index", 
                         color="#5b27d6", linewidth=2, linestyle='--')
            else:
                # Catch-all for any other columns
                plt.plot(data.index, data[col], label=col)


    plt.title(title, fontsize = 16, color = "black")
    plt.xlabel("Date")
    plt.legend(loc = "upper left")
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()

    # --- ADDING DATA SOURCE CAPTION --- #
    source_text = "Sources: S&P 500 (Kaggle: paveljurke) | Case-Shiller (FRED: CSUSHPINSA)"
    plt.figtext(0.5, 0.01, source_text, ha="center", fontsize=8, color="gray", style='italic')
    

    plt.savefig(f"static_plots/{filename}") 
    plt.close()