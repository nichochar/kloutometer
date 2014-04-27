from klout import Klout

k = Klout('hqaxmrn8p9x8aqmj7xvjm28q')

def get_klout_score(twtr_hand):
    # Get kloutId of the user by inputting a twitter screenName
    kloutId = k.identity.klout(screenName=twtr_hand).get('id')

    # Get klout score of the user
    score = k.user.score(kloutId=kloutId).get('score')

    return score
