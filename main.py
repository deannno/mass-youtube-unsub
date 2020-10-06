import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import json

scopes = ["https://www.googleapis.com/auth/youtube"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "REPLACE_WITH_CLIENT_SECRET_HERE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # get the list of subscribed channels
    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=50
    )
    subscriptions_dict = request.execute()
    
    with open("sample.json", "w") as outfile:  
        json.dump(subscriptions_dict, outfile) 

    # keep on doing this while there are still pages we're subscribed to
    while subscriptions_dict['pageInfo']['totalResults'] - subscriptions_dict['pageInfo']["resultsPerPage"] > -subscriptions_dict['pageInfo']["resultsPerPage"]:
        
        # get the list of subscribed channels
        request = youtube.subscriptions().list(
            part="snippet,contentDetails",
            mine=True,
            maxResults=50
        )
        subscriptions_dict = request.execute()
        
        # iterate through each subscribed channels
        for item in subscriptions_dict["items"]:
            ID = item['id'] 
            print(item['snippet']['title'], ID)

            # unsub from this channel
            request = youtube.subscriptions().delete(
                id=ID
            )
            response = request.execute()
            print(response)

if __name__ == "__main__":
    main()
