from extract_features.actions_involving_impression_session import ActionsInvolvingImpressionSession
from extract_features.change_impression_order_position_in_session import ChangeImpressionOrderPositionInSession
from extract_features.changes_of_sort_order_before_current import ChangeOfSortOrderBeforeCurrent
from extract_features.city_session import CitySession
from extract_features.city_session_populars_only import CitySessionPopularsOnly
from extract_features.classifier_parro import ClassifierParro
from extract_features.classifier_piccio import ClassifierPiccio
from extract_features.country_searched_session import CountrySearchedSession
from extract_features.day_moment_in_day import DayOfWeekAndMomentInDay
from extract_features.frenzy_factor_consecutive_steps import FrenzyFactorSession
from extract_features.impression_features import ImpressionFeature
from extract_features.impression_position_session import ImpressionPositionSession
from extract_features.impression_price_info_session import ImpressionPriceInfoSession
from extract_features.impression_rating import ImpressionRating
from extract_features.impression_rating_numeric import ImpressionRatingNumeric
from extract_features.impression_stars_numeric import ImpressionStarsNumeric
from extract_features.label import ImpressionLabel
from extract_features.last_action_involving_impression import LastInteractionInvolvingImpression
from extract_features.last_clickout_filters_satisfaction import LastClickoutFiltersSatisfaction
from extract_features.last_steps_before_clickout import StepsBeforeLastClickout
from extract_features.lazy_user import LazyUser
from extract_features.location_reference_percentage_of_clickouts import LocationReferencePercentageOfClickouts
from extract_features.location_reference_percentage_of_interactions import LocationReferencePercentageOfInteractions
from extract_features.num_impressions_in_clickout import NumImpressionsInClickout
from extract_features.num_times_item_impressed import NumTimesItemImpressed
from extract_features.perc_click_per_impressions import PercClickPerImpressions
from extract_features.personalized_top_pop import PersonalizedTopPop
#from extract_features.platform_features_similarty import PlatformFeaturesSimilarity
from extract_features.platform_reference_percentage_of_clickouts import PlatformReferencePercentageOfClickouts
from extract_features.platform_reference_percentage_of_interactions import PlatformReferencePercentageOfInteractions
from extract_features.platform_session import PlatformSession
from extract_features.price_info_session import PriceInfoSession
from extract_features.price_quality import PriceQuality
from extract_features.session_actions_num_ref_diff_from_impressions import SessionActionNumRefDiffFromImpressions
from extract_features.session_device import SessionDevice
from extract_features.session_filters_active_when_clickout import SessionFilterActiveWhenClickout
from extract_features.session_length import SessionLength
from extract_features.session_sort_order_when_clickout import SessionSortOrderWhenClickout
from extract_features.time_from_last_action_before_clk import TimeFromLastActionBeforeClk
from extract_features.time_per_impression import TimePerImpression
from extract_features.times_impression_appeared_in_clickouts_session import TimesImpressionAppearedInClickoutsSession
from extract_features.timing_from_last_interaction_impression import TimingFromLastInteractionImpression
from extract_features.top_pop_interaction_clickout_per_impression import TopPopInteractionClickoutPerImpression
from extract_features.top_pop_per_impression import TopPopPerImpression
from extract_features.top_pop_sorting_filters import TopPopSortingFilters
from extract_features.user_2_item import User2Item

import utils.menu as menu

if __name__ == '__main__':
    features_array = [
        ActionsInvolvingImpressionSession,
        #ChangeImpressionOrderPositionInSession,
        #ChangeOfSortOrderBeforeCurrent,
        #CitySession,
        CitySessionPopularsOnly,
        #ClassifierParro,
        #ClassifierPiccio,
        #CountrySearchedSession,
        #DayOfWeekAndMomentInDay,
        FrenzyFactorSession,
        #ImpressionFeature,
        ImpressionPositionSession,
        ImpressionPriceInfoSession,
        #ImpressionRating,
        ImpressionRatingNumeric,
        ImpressionStarsNumeric,
        ImpressionLabel,
        ImpressionFeature,
        #LastInteractionInvolvingImpression,
        #LastClickoutFiltersSatisfaction,
        #StepsBeforeLastClickout,
        LazyUser,
        LocationReferencePercentageOfClickouts,
        LocationReferencePercentageOfInteractions,
        NumImpressionsInClickout,
        NumTimesItemImpressed,
        PercClickPerImpressions,
        PersonalizedTopPop,
        #PlatformFeaturesSimilarity,
        PlatformReferencePercentageOfClickouts,
        PlatformReferencePercentageOfInteractions,
        PlatformSession,
        PriceInfoSession,
        PriceQuality,
        SessionActionNumRefDiffFromImpressions,
        SessionDevice,
        SessionFilterActiveWhenClickout,
        SessionLength,
        #SessionSortOrderWhenClickout,
        #TimeFromLastActionBeforeClk,
        TimePerImpression,
        TimesImpressionAppearedInClickoutsSession,
        #TimingFromLastInteractionImpression,
        TopPopInteractionClickoutPerImpression,
        TopPopPerImpression,
        #TopPopSortingFilters,
        User2Item,
    ]

    mode = menu.mode_selection()
    cluster = menu.cluster_selection()
    for f in features_array:
        feature = f(mode, cluster)
        feature.save_feature(overwrite_if_exists=False)

