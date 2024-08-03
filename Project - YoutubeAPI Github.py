#!/usr/bin/env python
# coding: utf-8

# In[5]:


from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns


# In[6]:


api_key = "Enter your API KEY"
#channel_ID = "UCj22tfcQrWG7EMEKS0qLeEg"
channel_ids = ['UCj22tfcQrWG7EMEKS0qLeEg', # Carry Minati
               'UCqwUrj10mAEsqezcItqvwEw', # Bhuvan Bam
               'UC7eHZXheF8nVOfwB2PEslMw', # Ashish Chanchlani
               'UC_vcKmg67vjMP7ciLnSxSHQ', # Amit Bhandana
               'UCt4atlExw8aj3Bm79nv1fig', # Round2Hell
               'UCMgapddJymOC6MBOiOqia1A', # Acharya Prashant
               'UCOhHO2ICt0ti9KAh-QHvttQ', # Technical Guruji
               'UCVmEbEQUGXHVm-O9pqa3JWg', # Harsh Beniwal
               'UCDwhsmzFDLc5hOB6SUglAjg', # Neetu Bisht
               'UCBqFKDipsnzvJdt6UT0lMIg' # Sandeep Maheshwari
              ]

youtube = build("youtube", "v3", developerKey=api_key)


# ## Functions to get channel statistics

# In[3]:


#def get_channel_stats(youtube, channel_ids):
#    request = youtube.channels().list(
#        part = "snippet, contentDetails, statistics",
#        id=channel_ids)
#    response = request.execute()
#    return response


# In[4]:


get_channel_stats(youtube, channel_ids)


# In[5]:


#def get_channel_stats(youtube, channel_ids):
#    request = youtube.channels().list(
#                 part = "snippet, contentDetails, statistics",
#                 id=channel_ids)
#    response = request.execute()
    
#    data = dict(Channel_name = response["items"][0]["snippet"]["title"],
#                Subscribers = response["items"][0]["statistics"]["subscriberCount"],
#                Views = response["items"][0]["statistics"]["viewCount"],
#                Total_videos = response["items"][0]["statistics"]["viewCount"])
#    return data


# In[6]:


#get_channel_stats(youtube, channel_ids)


# In[8]:


def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
                 part = "snippet, contentDetails, statistics",
                 id=','.join(channel_ids))
    response = request.execute()
    
    for i in range(len(response['items'])):
        data = dict(Channel_name = response["items"][i]["snippet"]["title"],
                    Subscribers = response["items"][i]["statistics"]["subscriberCount"],
                    Views = response["items"][i]["statistics"]["viewCount"],
                    playlist_ids = response["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"],
                    Total_videos = response["items"][i]["statistics"]["videoCount"])
                    
        all_data.append(data)
    
    
    return all_data


# In[11]:


channel_statistics = get_channel_stats(youtube, channel_ids)


# In[12]:


channel_statistics


# In[13]:


channel_data = pd.DataFrame(channel_statistics)


# In[14]:


channel_data


# In[15]:


channel_data.dtypes


# In[16]:


channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])


# In[17]:


channel_data.dtypes


# In[27]:


sns.set(rc={'figure.figsize':(22,10)})
ax = sns.barplot(x="Channel_name", y="Subscribers", data=channel_data)


# In[28]:


sns.set(rc={'figure.figsize':(19,10)})
ax = sns.barplot(x="Channel_name", y="Views", data=channel_data)


# In[29]:


sns.set(rc={'figure.figsize':(15,10)})
ax = sns.barplot(x="Channel_name", y="Total_videos", data=channel_data)


# ## Function to get video ids

# In[18]:


channel_data


# In[19]:


playlist_id = channel_data.loc[channel_data["Channel_name"] == "Neetu Bisht","playlist_ids"].iloc[0]
playlist_id


# In[20]:


def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
              part = "contentDetails",
              playlistId = playlist_id)
    response = request.execute()
    return response


# In[21]:


get_video_ids(youtube, playlist_id)


# In[22]:


def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
              part = "contentDetails",
              playlistId = playlist_id,
              maxResults = 50)
    response = request.execute()
    video_ids = []
    
    for i in range(len(response["items"])):
        video_ids.append(response["items"][i]["contentDetails"]["videoId"])
    
    next_page_token = response.get("nextPageTokens")
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                      part = "contentDetails",
                      playlistId = playlist_id,
                      maxResults = 50,
                      pageToken = next_page_token)
            response = request.execute()
            
            for i in range(len(response["items"])):
                video_ids.append(response["items"][i]["contentDetails"]["videoId"])
            
            next_page_token = response.get("nextPageToken")
    
    return (video_ids)


# In[23]:


video_ids = get_video_ids(youtube, playlist_id)


# In[24]:


video_ids


# ## Function to get dideo details

# In[31]:


def get_video_details(youtube, video_ids):
    all_video_stats = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
                    part = "snippet, statistics",
                    id = ",".join(video_ids[i:i+50]))
        response = request.execute()
        
        for video in response["items"]:
            video_stats = dict(Title =video["snippet"]["title"],
                               Published_date = video["snippet"]["publishedAt"],
                               Views = video["statistics"]["viewCount"],
                               Likes = video["statistics"]["likeCount"],
                               Comments = video["statistics"]["commentCount"]
                              )
            all_video_stats.append(video_stats)
        
    return len(all_video_stats)


# In[32]:


get_video_details(youtube, video_ids)


# In[33]:


#def get_video_details(youtube, video_ids):
#    all_video_stats = []
    
#    for i in range(0, len(video_ids), 50):
#        request = youtube.videos().list(
#                    part = "snippet, statistics",
#                    id = ",".join(video_ids[i:i+50]))
#        response = request.execute()
#        
#        for video in response["items"]:
#            video_stats = dict(Title =video["snippet"]["title"],
#                               Published_date = video["snippet"]["publishedAt"],
#                               Views = video["statistics"]["viewCount"],
#                               Likes = video["statistics"]["likeCount"],
#                               Comments = video["statistics"]["commentCount"]
#                               )
#            all_video_stats.append(video_stats)
#        
#    return all_video_stats


# In[34]:


#get_video_details(youtube, video_ids)


# In[38]:


""""def get_video_details(youtube, playlist_id):
    all_video_stats = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        video_ids = [item["snippet"]["resourceId"]["videoId"] for item in response["items"]]

        video_request = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids)
        )
        video_response = video_request.execute()

        for video in video_response["items"]:
            video_stats = dict(
                Title=video["snippet"]["title"],
                Published_date=video["snippet"]["publishedAt"],
                Views=video["statistics"]["viewCount"],
                Likes=video["statistics"]["likeCount"],
                Comments=video["statistics"]["commentCount"]
            )
            all_video_stats.append(video_stats)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return all_video_stats"""


# In[39]:


'''get_video_details(youtube, playlist_id)'''


# In[45]:


def get_video_details(youtube, playlist_id):
    all_video_stats = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        video_ids = [item["snippet"]["resourceId"]["videoId"] for item in response["items"]]

        video_request = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids)
        )
        video_response = video_request.execute()

        for video in video_response["items"]:
            video_stats = dict(
                Title=video["snippet"]["title"],
                Published_date=video["snippet"]["publishedAt"],
                Views=video["statistics"].get("viewCount"),
                Likes=video["statistics"].get("likeCount"),
                Comments=video["statistics"].get("commentCount")
            )
            all_video_stats.append(video_stats)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return all_video_stats


# In[46]:


get_video_details(youtube, playlist_id)


# In[51]:


video_details = get_video_details(youtube, playlist_id)
video_data = pd.DataFrame(video_details)
#headers = ["Title", "Published_date", "Views", "Likes", "Comments"]
#df = pd.DataFrame(video_details, columns=headers)


# In[52]:


video_data


# In[50]:


#df.to_csv('C:/Users/barbi/Downloads/Aman Power BI/Youtube API Project dataset/video_details.csv', index=False)


# In[56]:


video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Comments'] = pd.to_numeric(video_data['Comments'])


# In[57]:


video_data


# ## Top 10 Videos

# In[58]:


top10_videos = video_data.sort_values(by = "Views", ascending = False).head(10)
top10_videos


# In[59]:


#sns.set(rc={'figure.figsize':(15,10)})
ax1 = sns.barplot(x="Views", y="Title", data=top10_videos)


# In[60]:


video_data["Month"] = pd.to_datetime(video_data["Published_date"]).dt.strftime("%b")
video_data


# In[61]:


videos_per_month = video_data.groupby("Month", as_index=False).size()
videos_per_month


# In[62]:


#months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#videos_per_month['Month'] = pd.Categorical(videos_per_month['Month'], categories=months_order, ordered=True)


# In[63]:


#Sort by the defined order
videos_per_month = videos_per_month.sort_values('Month')


# In[64]:


#videos_per_month


# In[69]:


months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories=months_order, ordered=True)


# In[70]:


videos_per_month = videos_per_month.sort_index()


# In[71]:


videos_per_month


# In[72]:


ax2 = sns.barplot(x="Month", y="size", data=videos_per_month)


# In[ ]:




