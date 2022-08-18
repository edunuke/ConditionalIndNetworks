"""
Description: Code that computes conditional independence networks
Author: Eduardo Perez Denadai
Date: 15-8-2022
"""
import numpy as np
import pandas as pd
import networkx as nx
from sklearn import manifold
from sklearn import covariance
import matplotlib.pylab as plt
from sklearn.utils.validation import check_array
from sklearn.base import BaseEstimator



class PartialCorrelations(BaseEstimator):
    """ Discovering relations in observational data is difficult for many reasons 
        (noise, non causal, non-experimental, etc.)
        Here we perform conditional independence netowrk method for descovering potential 
        associations among the variables by building Conditional Independence Network 
        through partial correlation matrices via precision matrices.

    Parameters
    ----------
    edge_model : object, default = covariance.EmpiricalCovariance() 
        takes the covariance object model 

    """
    def __init__(self, edge_model = None):
        
        # set the initial edge and node models
        if edge_model is None: 
            edge_model= covariance.EmpiricalCovariance()

        self.edge_model  = edge_model



    def fit(self, X, y=None):
        """ A reference implementation of a fitting function.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,) or (n_samples, n_outputs)
            The target values (class labels in classification, real numbers in
            regression).
        Returns
        -------
        self : object
            Returns self.
        """
        self.names = X.columns.values
        self.X = check_array(X, accept_sparse=True)
        self.edge_model.fit(self.X)


        # use precision matrix to compute partial correlations
        self.partial_correlations_ = self.edge_model.precision_.copy()
        d = 1 / np.sqrt(np.diag(self.partial_correlations_))
        self.partial_correlations_ *= d
        self.partial_correlations_ *= d[:, np.newaxis]
        
        if isinstance(self.edge_model,covariance.GraphicalLassoCV):
            self.cv_results_ = self.edge_model.cv_results_
            self.alpha_ = self.edge_model.alpha_

        
        self.is_fitted_ = True

        return self



    def compute_cond_ind_matrix(self,threshold=0.3): 
        """ Computes sparse partial correlations or 
        conditional independence adjacency matrix using
        hard thresholding.

        Parameters
        ----------
        threshold : float, default = None
            Hrd threshold for building the CI adjacency matrix
            
        Returns
        -------
        DataFrame


        """          
        #upper diagonals
        non_zero = np.abs(np.triu(self.partial_correlations_, k=1)) 
        if threshold is None:
            return pd.DataFrame(data = non_zero, 
                                columns = self.names, 
                                index=self.names)
        else:
            # sparsify to get conditional independence adj matrix
            non_zero = non_zero > threshold # < ---- thresholding
            return pd.DataFrame(data = non_zero.astype(int), 
                                columns = self.names, 
                                index=self.names)
    


    def plot_cond_ind_network(self, threshold=0.3,figsize=(15,15)):
        """ plots the conditional independence adjacency matrix using
        hard thresholding.

        Parameters
        ----------
        threshold : float, default = None
            Hrd threshold for building the CI adjacency matrix
            
        Returns
        -------
        None
        """

        cond_ind_matrix = self.compute_cond_ind_matrix(threshold=threshold)
        partial_corr_matrix = self.compute_cond_ind_matrix(threshold=None)
        weight_matrix = cond_ind_matrix*partial_corr_matrix
        G=nx.Graph(self.compute_cond_ind_matrix(threshold=threshold))
        edges = G.edges(data=True)

        kv_pairs = dict([(x,y) for x,y, in zip(weight_matrix.columns, range(len(weight_matrix.columns)))])
        edge_pairs = list(G.edges())
        mapping = []

        for p1, p2 in edge_pairs:
            mapping.append((kv_pairs[p1], kv_pairs[p2]))
        
        weights = np.array([weight_matrix.iloc[x] for x in mapping])
        plt.figure(3,figsize=figsize)
        pos = nx.circular_layout(G)
        
        nx.set_edge_attributes(G, 
                               values=dict([(x,np.round(y,2)) for x,y in zip(edge_pairs,weights)]),
                               name="weight")

        labels = nx.get_edge_attributes(G, "weight")

        
        nx.draw_networkx(G, pos=pos, with_labels=True, arrowstyle='-', 
                        edge_color=weights, width=10*weights)
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels)
        plt.title(f"Conditional Independence Network\n Threshold: {threshold}")
        plt.show()