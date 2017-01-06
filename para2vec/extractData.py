import tweepy
import time
def auth_api():
    key_tokens = {}

    key_tokens['consumer_key'] = ''
    key_tokens['consumer_secret'] = ''
    key_tokens['access_token'] = ''
    key_tokens['access_secret'] = ''

    auth_twitter = tweepy.OAuthHandler(key_tokens['consumer_key'],key_tokens['consumer_secret'])
    auth_twitter.set_access_token(key_tokens['access_token'],key_tokens['access_secret'])
    api_twitter = tweepy.API(auth_twitter)

    return api_twitter

def getTweets(uid, api_twitter, limit = None):

    try:
        time.sleep(1)
        return api_twitter.user_timeline(user_id = uid, count = limit)
    except tweepy.error.RateLimitError:
        print("tweepy.error.RateLimitError")
        return None
    except tweepy.error.TweepError:
        print("error in requesting")
        return None

def getFriend(uid, api_twitter):

    try:
        time.sleep(1)
        return api_twitter.friends_ids(id = uid), api_twitter.followers_ids(id = uid)
    except tweepy.error.RateLimitError:
        print("tweepy.error.RateLimitError")
        return None
    except tweepy.error.TweepError:
        print("error in requesting")
        return None

def userTweets(id_List,api_twitter):
    tweetsDict = {}
    geoDict = {}
    for id in id_List:
        tweetsList = getTweets(id, api_twitter)

        if len(tweetsList) > 200:
            tpList = []
            geoLocation = []
            location_list = [rawtweet._json['coordinates'] for rawtweet in tweetsList if rawtweet._json['coordinates']]
            if len(location_list) == 0:
                geo = [rawtweet._json['geo'] for rawtweet in tweetsList if rawtweet._json['geo']]
                if len(geo) !=0:
                    geoLocation = geo
                else:
                    place = [rawtweet._json['place'] for rawtweet in tweetsList if rawtweet._json['place']]
                    if len(place) !=0:
                        geoLocation = place
                    else:
                        pass

            else:
                geoLocation =  location_list
            for tts in tweetsList:
                tpList.append(tts.text)

            tweetsDict[id] = tpList
            geoDict[id] = geoLocation
    return tweetsDict, geoDict

def userFriends(id_List,api_twitter):
    dict = {}
    for id in id_List:
        friendsList = getFriend(id, api_twitter)
        dict[id] = friendsList
    return dict




