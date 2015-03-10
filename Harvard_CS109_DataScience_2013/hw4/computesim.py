import numpy as np

from mrjob.job import MRJob
from itertools import combinations, permutations

from scipy.stats.stats import pearsonr


class RestaurantSimilarities(MRJob):

    def steps(self):
        "the steps in the map-reduce process"
        thesteps = [
            self.mr(mapper=self.line_mapper, reducer=self.users_items_collector),
            self.mr(mapper=self.pair_items_mapper, reducer=self.calc_sim_collector)
        ]
        return thesteps

    def line_mapper(self,_,line):
        "this is the complete implementation"
        user_id,business_id,stars,business_avg,user_avg=line.split(',')
        yield user_id, (business_id,stars,business_avg,user_avg)


    def users_items_collector(self, user_id, values):
        """
        #iterate over the list of tuples yielded in the previous mapper
        #and append them to an array of rating information
        """
        result_vals = [(b_id, float(stars)-float(u_avg)) for b_id,stars,b_avg,u_avg in values]
        yield user_id, result_vals

    def pair_items_mapper(self, user_id, values):
        """
        ignoring the user_id key, take all combinations of business pairs
        and yield as key the pair id, and as value the pair rating information
        """
        b_id, ratings = zip(*values)
        sort_idx = np.argsort(b_id)
        pairs_idx = combinations(sort_idx,2)
        for idx1, idx2 in pairs_idx:
            result_key = (b_id[idx1], b_id[idx2])
            result_vals = (ratings[idx1], ratings[idx2])
            yield result_key, result_vals

    def calc_sim_collector(self, key, values):
        """
        Pick up the information from the previous yield as shown. Compute
        the pearson correlation and yield the final information as in the
        last line here.
        """

	    #your code here
        (rest1, rest2), common_ratings = key, values
        rest1_reviews, rest2_reviews = zip(*common_ratings)

        rho = pearsonr(rest1_reviews, rest2_reviews)[0]

        if np.isnan(rho):
            rho = 0
            
        n_common = len(rest1_reviews)
        
        yield (rest1, rest2), (rho, n_common)


#Below MUST be there for things to work
if __name__ == '__main__':
    RestaurantSimilarities.run()