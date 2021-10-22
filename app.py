import tweepy
import requests
import os

def sort_database(names_of_images):
    names_of_images.sort()
    with open('database.txt', 'w') as file:
        for name in names_of_images:
            file.write(f'{name}\n')

if __name__ == '__main__':
    with open('tokens.txt', 'r') as file:
        api_key = file.readline().split('/')[0]
        api_secret_key = file.readline().split('/')[0]
        access_token = file.readline().split('/')[0]
        access_token_secret = file.readline().split('/')[0]

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets = tweepy.Cursor(
        api.user_timeline,
        exclude_replies=True
        ).items(30)

    images_already_downloaded = []

    with open('database.txt', 'r') as file:
        for line in file.readlines():
            images_already_downloaded.append(line.strip('\n'))


    for tweet in tweets:
        if (tweet.text.split(' ')[0].lower() == 'rt'):
            if 'media' in tweet.entities:
                media_entities = tweet.entities['media']
            else:
                print('The element doesn\'t have a media entity.')
                continue
            image_url = ''
            for item in media_entities:
                if item['media_url']:
                    image_url = item['media_url']

            image_name = image_url.split('/')[-1]
            path = r'D:\Enrico\Imagens\RTs'   

            images_in_folder = os.listdir(path)

            if image_name in images_in_folder:
                print('The image was already downloaded')    

            else:    
                image = requests.get(image_url)
                
                with open(os.path.join(path, image_name), 'wb') as file:
                    file.write(image.content)

                images_already_downloaded.append(image_name)

    sort_database(images_already_downloaded)