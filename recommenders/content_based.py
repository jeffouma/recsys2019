from recommenders.distance_based_recommender import DistanceBasedRecommender
import data

class ContentBased(DistanceBasedRecommender):
    """
    Computes the recommendations for a user by looking for the similar users based on the
    item which they rated
    """

    def __init__(self, mode='full', urm_name='urm_clickout', k=100, distance='cosine', shrink=0,
                 threshold=0, implicit=False, alpha=0.5, beta=0.5, l=0.5, c=0.5):
        """
        Initialize the model

        Parameters
        ----------
        k: int
            K nearest neighbour to consider.
        distance: str
            One of the supported distance metrics, check collaborative_filtering_base constants.
        shrink: float, optional
            Shrink term used in the normalization
        threshold: float, optional
            All the values under this value are cutted from the final result
        implicit: bool, optional
            If true, treat the URM as implicit, otherwise consider explicit ratings (real values) in the URM
        alpha: float, optional, included in [0,1]
        beta: float, optional, included in [0,1]
        l: float, optional, balance coefficient used in s_plus distance, included in [0,1]
        c: float, optional, cosine coefficient, included in [0,1]
        """
        urm = data.urm(mode, urm_name=urm_name)
        icm = data.icm()
        super(ContentBased, self).__init__(icm,
                                          mode=mode,
                                          urm_name=urm_name,
                                          k=k,
                                          distance=distance,
                                          shrink=shrink,
                                          threshold=threshold,
                                          implicit=implicit,
                                          alpha=alpha,
                                          beta=beta,
                                          l=l,
                                          c=c,
                                          urm=urm,
                                          matrix_mul_order='standard')

        self.name = 'content based: k: {} distance: {} shrink: {} threshold: {} implicit: {} alpha: {} beta: {} ' \
                    'l: {} c: {}'.format(k, distance, shrink, threshold, implicit, alpha, beta, l, c)
