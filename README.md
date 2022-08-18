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

## Full Dependence model among covariates + target carries no information gain (threshold = 1.0)

![Full Dependence (No information gain)](https://github.com/edunuke/ConditionalIndNetworks/blob/main/img/full%20dependence%20plot.png)


## Full Independence model among covariates + target also carries no information gain (threshold = 0.0)

![Full Inependence (No information gain)](https://github.com/edunuke/ConditionalIndNetworks/blob/main/img/full%20dependence%20plot.png)

## Final associative structure model among covariates + target carries no information gain (threshold = 0.35)

![Thresholded Model](https://github.com/edunuke/ConditionalIndNetworks/blob/main/img/thresholded%20structure.png)!



From the last plot we can make the following observations:

1. AveRooms and AveBedrms are strongly related to each other and together represents a latent concept which is House Size.
2. This latent concept of House size has a strong association with MedInc (Median Income)
3. MedInc is strongly associated with the target (house price)
4. Latitude and Longitude are strongly associated and together represent a latent concept which is Position/Localization
5. Position is strongly associated with the target (house price)
6. Population, House Age, and Average Occupancy are not related to each other, other variables nor the target.

The final structre makes a lot of sense for the dataset which helps validates expert knowledge gained during the problem understanding phase of a project. It is important to understand that this is not a causal model, hence no directed components, as the dataset is purely observational. However, the analyst and the expert broker can validate with their knowledge the structure. The role of the analyst is to choose a threshold that more or less represents the degree of belief in the associations presented given the dataset.
