# Rate of new tuberculosis cases analysis

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)


**Author:** Marita Heidl (ID: `i6406044`)  
**Course:** MAT2007 – Introduction to Programming  
**University:** Maastricht Science Programme, Maastricht University  

---

## Table of Contents
- [01. Description](#-description)
- [02. Repository structure](#-repository-structure)
- [03. Dataset information & preprocessing](#-dataset-information--preprocessing)
- [04. Installation & requirements](#-installation--requirements)
- [05. How to run the code](#-how-to-run-the-code)
- [06. Reproducibility & results](#-reproducibility--results)
- [07. Statistical methods](#-statistical-methods)

---

## 01. Description
This project looks at global surveillance records of **new tuberculosis (TB) cases per 100,000 individuals** to evaluate:
1. **Cross-sectional lead (2024):** Which nations had the highest incidence rates in 2024, and whether the margin between the two leading Countries is statistically significant.
2. **COVID-19 Disruption:** How the COVID-19 pandemic (2020–2021) impacted reported incidence rates in the highest-burden nation (Kiribati).

---

## 02. Repository structure

* `incidence-of-tuberculosis-sdgs.csv` — Raw dataset from Our World in Data
* `project TB.py` — Main analysis and plotting script
* `figures/` — Directory containing generated plots
  * `plot_1.png` — Top 5 countries bar chart (2024)
  * `plot_2.png` — Kiribati COVID-19 trendline (2016–2024)
* `main.tex` — LaTeX report source code
* `main.pdf` — Compiled final PDF report
* `README.md` — Project documentation


---

## 03. Dataset information & preprocessing

The dataset used in this project is:
**Rate of new tuberculosis cases** 

**Source**: World Health Organisation (WHO) Global Tuberculosis Programme, accessed via Our World in Data.



**Link**: 
Our world in data https://ourworldindata.org/tuberculosis

**File**: `incidence-of-tuberculosis-sdgs.csv`

Raw columns:
* `Entity`: Geographic territory 
* `Code`: Country ISO code or regional aggregate identifier
* `Year`: Observation year (1990-2024)
* `Estimated incidence of all forms of tuberculosis`: Rate per 100.000 individuals

Data cleaning not required!

The raw dataset contains non-sovereign aggregates. The script automatically cleans the data:

1. Drops missing ISO codes 
2. Retains strictly standard three-letter ISO codes 


---
## 04. Installation & requirements
**Python 3.8** or higher is required.

The following Python libraries are used:
* numpy
* pandas
* matplotlib

If these libraries are not already installed, they can be installed using:
``` bash
pip install numpy pandas matplotlib
```


--- 
## 05. How to run the code
Clone the repository:

git clone [https://github.com/maritaheidl/MAT2007-project.git](https://github.com/maritaheidl/MAT2007-project.git)
cd MAT2007-project 

Verify dataset placement:

Make sure that `incidence-of-tuberculosis-sdgs.csv` is located in the root project folder along with `project TB.py`

Execute the script:
```bash
python "project TB.py"
```

---
## 06. Reproducibility & results
If `project TB.py` is ran, the program will:

1. Automatically generate the directory `figures/` if it does not exist.
2. Generate and save high-resolution figures: 
* `figures/plot_1.png` : Top 5 countries in 2024 with uncertainty bars
* `figures/plot_2.png` : 2016-2024 time series of Kiribati highlighting the 2020 - 2021 COVID-19 period.
3. Open visualisation windows sequentially (`plt.show()`).
4. Output calculated statistical metrics directly in the terminal: 

Equations results:
* $R_1$ (Kiribati): 945.00 +/- 30.74
* $R_2$ (Papua New Guinea): 664.00 +/- 25.77
* $\Delta R(Difference): 281.00 +/- 40.11

* Shift from 2019 to 2020: -60.00 per 100k

Generated files:
* `figures/plot_1.png`
* `figures/plot_2.png`
---
## 07. Statistical methods

This project applies standard statistical and uncertainty propagation techniques to analyze tuberculosis incidence rates ($R$ per 100,000 population):

### 1. Counting Uncertainty (Poisson Model)
 Incidence counts are modeled as Poisson statistics. The statistical uncertainty $\sigma$ associated with an estimated rate $R$ is calculated as:

$$\sigma = \sqrt{R}$$

### 2. Uncertainty propagation 
To evaluate the absolute margin $\Delta R$ between the two highest-burden nations (Kiribati $R_1$ and Papua New Guinea $R_2$):

$$\Delta R = R_1 - R_2$$

Assuming independent, uncorrelated measurements, the propagated standard error $\sigma_{\Delta R}$ is determined by combining uncertainties in quadrature:

$$\sigma_{\Delta R} = \sqrt{\sigma_1^2 + \sigma_2^2}$$

### 3. Hypothesis testing ($z$-score)
To assess whether the observed lead of Kiribati over Papua New Guinea is  statistically significant rather than a random fluctuation, a standardized two-sample $z$-score is computed:

$$z = \frac{\Delta R}{\sigma_{\Delta R}}$$

* **Significance Threshold:** A standard significance threshold of $z \ge 3.0\sigma$ ($p < 0.003$) was used.
* **Result:** With $z = 7.01\sigma$, the null hypothesis ($H_0: R_1 = R_2$) is rejected, confirming that Kiribati’s higher incidence is statistically significant.
