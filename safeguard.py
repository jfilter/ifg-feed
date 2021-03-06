import re

import yaml
from twython import Twython


def sane_timeline():
    """Check if there no duplicated links in the past 200 tweets.

    Returns:
        True if there are no duplicates and False, otherwise
    """
    with open('/home/jfilter/code/ifg-feed/ttnconfig/config.yaml') as f:
        config = yaml.load(f)

    api_key, api_secret, oauth_token, oauth_secret = [config['twitter'][k] for k in (
        'api_key', 'api_secret', 'oauth_token', 'oauth_secret')]

    client_args = {
        'timeout': 300,
    }

    try:
        twitter = Twython(api_key, api_secret,
                      oauth_token, oauth_secret, client_args=client_args)
        tweets = twitter.get_user_timeline(count=200)
    except expression as identifier:
        print('error while getting previous tweets, but whatever:', identifier)
        return True
    
    all_urls = []

    for t in tweets:
        text = t['text']
        # it should always match but for some reason it isn't
        cleaned_text = text
        if ':' in text:
            index_match = text.index(':')
            cleaned_text = text[index_match + 1:]
        else:
            print('not able to match ":" in\n' + text)
        urls = re.findall(r'(https?://\S+)', cleaned_text)
        all_urls += urls
    #for l in all_urls:
    #    if all_urls.count(l) > 1:
    #         print(l)
    return len(all_urls) == len(set(all_urls))


if __name__ == '__main__':
    print(sane_timeline())
