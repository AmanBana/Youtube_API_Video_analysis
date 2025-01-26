#!/usr/bin/env python
# coding: utf-8

# In[5]:


from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

# Step 1: Initialize the YouTube API
api_key = "Enter your API KEY"
youtube = build("youtube", "v3", developerKey=api_key)

# Step 2: Define channel IDs
channel_ids = [
    'UCj22tfcQrWG7EMEKS0qLeEg',  # Carry Minati
    'UCqwUrj10mAEsqezcItqvwEw',  # Bhuvan Bam
    'UC7eHZXheF8nVOfwB2PEslMw',  # Ashish Chanchlani
    'UC_vcKmg67vjMP7ciLnSxSHQ',  # Amit Bhandana
    'UCt4atlExw8aj3Bm79nv1fig',  # Round2Hell
    'UCMgapddJymOC6MBOiOqia1A',  # Acharya Prashant
    'UCOhHO2ICt0ti9KAh-QHvttQ',  # Technical Guruji
    'UCVmEbEQUGXHVm-O9pqa3JWg',  # Harsh Beniwal
    'UCDwhsmzFDLc5hOB6SUglAjg',  # Neetu Bisht
    'UCBqFKDipsnzvJdt6UT0lMIg'   # Sandeep Maheshwari
]

# Step 3: Function to get channel statistics
def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
        part="snippet, contentDetails, statistics",
        id=','.join(channel_ids)
    )
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(
            Channel_name=response["items"][i]["snippet"]["title"],
            Subscribers=response["items"][i]["statistics"]["subscriberCount"],
            Views=response["items"][i]["statistics"]["viewCount"],
            playlist_ids=response["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"],
            Total_videos=response["items"][i]["statistics"]["videoCount"]
        )
        all_data.append(data)

    print("Channel statistics fetched successfully.")
    return all_data

# Step 4: Fetch and display channel statistics
channel_statistics = get_channel_stats(youtube, channel_ids)
print(channel_statistics)

# Step 5: Convert channel statistics to a DataFrame
print("Converting channel statistics to a DataFrame...")
channel_data = pd.DataFrame(channel_statistics)
print(channel_data)

# Step 6: Convert data types for numeric fields
print("Converting numeric fields to appropriate data types...")
channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])
print(channel_data.dtypes)

# Step 7: Visualize channel statistics
print("Visualizing Subscribers per channel...")
sns.set(rc={'figure.figsize': (22, 10)})
sns.barplot(x="Channel_name", y="Subscribers", data=channel_data)

print("Visualizing Views per channel...")
sns.set(rc={'figure.figsize': (19, 10)})
sns.barplot(x="Channel_name", y="Views", data=channel_data)

print("Visualizing Total Videos per channel...")
sns.set(rc={'figure.figsize': (15, 10)})
sns.barplot(x="Channel_name", y="Total_videos", data=channel_data)

# Step 8: Get video IDs from a specific channel
print("Getting video IDs for a specific channel (e.g., Neetu Bisht)...")
playlist_id = channel_data.loc[channel_data["Channel_name"] == "Neetu Bisht", "playlist_ids"].iloc[0]
print(f"Playlist ID for Neetu Bisht: {playlist_id}")

def get_video_ids(youtube, playlist_id):
    print("Fetching video IDs...")
    video_ids = []
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    for i in range(len(response["items"])):
        video_ids.append(response["items"][i]["contentDetails"]["videoId"])

    next_page_token = response.get("nextPageToken")
    while next_page_token:
        print("Fetching more video IDs...")
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for i in range(len(response["items"])):
            video_ids.append(response["items"][i]["contentDetails"]["videoId"])

        next_page_token = response.get("nextPageToken")

    print(f"Total videos fetched: {len(video_ids)}")
    return video_ids

video_ids = get_video_ids(youtube, playlist_id)
print("Video IDs fetched:")
print(video_ids)

# Step 9: Get video details
def get_video_details(youtube, video_ids):
    print("Fetching video details...")
    all_video_stats = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids[i:i + 50])
        )
        response = request.execute()

        for video in response["items"]:
            video_stats = dict(
                Title=video["snippet"]["title"],
                Published_date=video["snippet"]["publishedAt"],
                Views=video["statistics"].get("viewCount"),
                Likes=video["statistics"].get("likeCount"),
                Comments=video["statistics"].get("commentCount")
            )
            all_video_stats.append(video_stats)

    print("Video details fetched successfully.")
    return all_video_stats

video_details = get_video_details(youtube, video_ids)
print("Video Details:")
print(video_details)

# Step 10: Convert video details to DataFrame
print("Converting video details to a DataFrame...")
video_data = pd.DataFrame(video_details)
video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Comments'] = pd.to_numeric(video_data['Comments'])
print(video_data)

# Step 11: Visualize top 10 videos by views
print("Visualizing top 10 videos by views...")
top10_videos = video_data.sort_values(by="Views", ascending=False).head(10)
sns.barplot(x="Views", y="Title", data=top10_videos)

# Step 12: Analyze videos per month
print("Analyzing videos per month...")
video_data["Month"] = pd.to_datetime(video_data["Published_date"]).dt.strftime("%b")
videos_per_month = video_data.groupby("Month", as_index=False).size()
months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories=months_order, ordered=True)
videos_per_month = videos_per_month.sort_index()
sns.barplot(x="Month", y="size", data=videos_per_month)
