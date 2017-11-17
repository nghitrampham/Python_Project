
"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from ucb import main, trace, interact
from utils import distance, mean, zip, enumerate, sample
from visualize import draw_map

##################################
# Phase 2: Unsupervised Learning #
##################################


def find_closest(location, centroids):
    """Return the centroid in centroids that is closest to location.
    If multiple centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    """
    #List contains the distance from location to each value in centroids
    disList = [distance(location, centroids[i]) for i in range(len(centroids))]
    #Find the index which contains the min distance and return the corresponding centroid
    return centroids[disList.index(min(disList))]




def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]


def group_by_centroid(restaurants, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. Each item in
    restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.
    """

    # Initializing a list that will keep lists of pair of centroid and restaurant
    list_key_value =[]
    for restaurant in restaurants:
        closest_centroid = find_closest(restaurant_location(restaurant),centroids)
        # create pair of centroid and restaurant
        list_key_value.append([closest_centroid,restaurant])
        # group restaurants that have the same centroids
    return group_by_first(list_key_value)



def find_centroid(cluster):
    """Return the centroid of the locations of the restaurants in cluster."""

    # Initializing the list of latitude and longitude that keep the data for all
    # restaurants
    latitude = []
    longitude = []
    for restaurant in cluster:
        latitude.append(restaurant_location(restaurant)[0])
        longitude.append(restaurant_location(restaurant)[1])
    # find average latitude and longitude
    aver_latitude = mean(latitude)
    aver_longitude = mean(longitude)

    return [aver_latitude,aver_longitude]


def k_means(restaurants, k, max_updates=100):
    """Use k-means to group restaurants by location into k clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]
    while old_centroids != centroids and n < max_updates:
        # initializing new centroids
        new_centroids = []
        old_centroids = centroids
        # return a group of restaurants that have same centroid
        groups = group_by_centroid(restaurants, centroids)
        for group in groups:
            new_centroids.append(find_centroid(group))
        # Bind centroids to a new list of the centroids of all the clusters
        centroids = new_centroids
        n += 1
    return centroids


################################
# Phase 3: Supervised Learning #
################################


def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    reviews_by_user = {review_restaurant_name(review): review_rating(review)
                       for review in user_reviews(user).values()}

    xs = [feature_fn(r) for r in restaurants]
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants]

    #Calculate mean of the xs and ys
    x_mean = mean(xs)
    y_mean = mean(ys)

    Sxx = sum([(x-x_mean)**2 for x in xs])
    Syy = sum([(y-y_mean)**2 for y in ys])
    Sxy = sum([(x-x_mean)*(y-y_mean) for x,y in zip(xs,ys)])

    #Calculating a,b, and r_square
    b = Sxy/Sxx
    a = mean(ys) - b*mean(xs)
    r_squared = Sxy**2/(Sxx*Syy)

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared


def best_predictor(user, restaurants, feature_fns):
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    reviewed = user_reviewed_restaurants(user, restaurants)

    #Initialize an empty dictionary to store pair r_squared and prediction
    #for each feature functions
    r_squared = {}

    # Loop through each feature to see which one gives the highest r_square
    for i in feature_fns:
        values = find_predictor(user, reviewed, i)
        r_squared[values[1]] = values[0]
    return r_squared[max(r_squared)]

def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of restaurants by user using the best
    predictor based on a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """
    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    reviewed = user_reviewed_restaurants(user, restaurants)

    #Initialize empty dictionary to store pair value restaurant names and ratings
    user_dic = {}
    #Loop through each restaurant to match the rating
    for restaurant in restaurants:
        name = restaurant_name(restaurant)
        #If the user rated the restaurant before, find the rate and pair with the restaurant name
        if i in reviewed:
            user_dic[name] = user_rating(user, name)
        #If not, use predictor to calculate the rating
        else:
            user_dic[name] = predictor(restaurant)
    return user_dic


def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    return [i for i in restaurants if query in restaurant_categories(i)]


def feature_set():
    """Return a sequence of feature functions."""
    return [lambda r: mean(restaurant_ratings(r)),
            restaurant_price,
            lambda r: len(restaurant_ratings(r)),
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]


@main
def main(*args):
    import argparse
    parser = argparse.ArgumentParser(
        description='Run Recommendations',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-u', '--user', type=str, choices=USER_FILES,
                        default='test_user',
                        metavar='USER',
                        help='user file, e.g.\n' +
                        '{{{}}}'.format(','.join(sample(USER_FILES, 3))))
    parser.add_argument('-k', '--k', type=int, help='for k-means')
    parser.add_argument('-q', '--query', choices=CATEGORIES,
                        metavar='QUERY',
                        help='search for restaurants by category e.g.\n'
                        '{{{}}}'.format(','.join(sample(CATEGORIES, 3))))
    parser.add_argument('-p', '--predict', action='store_true',
                        help='predict ratings for all restaurants')
    parser.add_argument('-r', '--restaurants', action='store_true',
                        help='outputs a list of restaurant names')
    args = parser.parse_args()

    # Output a list of restaurant names
    if args.restaurants:
        print('Restaurant names:')
        for restaurant in sorted(ALL_RESTAURANTS, key=restaurant_name):
            print(repr(restaurant_name(restaurant)))
        exit(0)

    # Select restaurants using a category query
    if args.query:
        restaurants = search(args.query, ALL_RESTAURANTS)
    else:
        restaurants = ALL_RESTAURANTS

    # Load a user
    assert args.user, 'A --user is required to draw a map'
    user = load_user_file('{}.dat'.format(args.user))

    # Collect ratings
    if args.predict:
        ratings = rate_all(user, restaurants, feature_set())
    else:
        restaurants = user_reviewed_restaurants(user, restaurants)
        names = [restaurant_name(r) for r in restaurants]
        ratings = {name: user_rating(user, name) for name in names}

    # Draw the visualization
    if args.k:
        centroids = k_means(restaurants, min(args.k, len(restaurants)))
    else:
        centroids = [restaurant_location(r) for r in restaurants]
    draw_map(centroids, restaurants, ratings)
