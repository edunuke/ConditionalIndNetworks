# ConditionalIndNetworks
Conditional independence network for associative structure discovery

# Description

This simple module produces Conditional Independence Networks computed from partial correlations and hard thresholding.
This method is valid under certain statistical assumptions. 

Please see:

[Partial correlation and conditional correlation as measure of conditional independence](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-842X.2004.00360.x)

# Usage

See example notebook

# Example Results and Interpretation

This is a Exploratory Data Analysis technique that is able to visually guide the discovery of associative structures in datasets which can help you build more interpretable models at the problem understanding and data exploration phase. The method is simple yet powerful given some important sets of assumptions (see paper referenced).

1. Load data Target + Covariates or Covariates only
2. Perform power transform to make data more gaussian-like
3. Load the module and fit the PartialCorrelations Model
4. Explore the plots (see below from the California Housing Prices Dataset) and tune the thresholds


![Full Dependence (No information gain)](https://github.com/edunuke/ConditionalIndNetworks/blob/main/img/full%20dependence%20plot.png)

![Thresholded Model](https://github.com/edunuke/ConditionalIndNetworks/blob/main/img/thresholded%20structure.png)!

![Full Inependence (No information gain)](https://github.com/edunuke/ConditionalIndNetworks/blob/main/img/full%20dependence%20plot.png)

