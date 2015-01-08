import re
import time
from google.appengine.api import urlfetch

def current_time():
  
  # Return current UTC time in readable format
  return(time.ctime())


def youtube_list():

  # Fetch your youtube videos page
  url = "https://www.youtube.com/user/SchibleyJ/videos?flow=grid"
  result = urlfetch.fetch(url)

  # If fetch was successful  
  if result.status_code == 200:
    output = ''

    # Strip off stuff at top of page
    content = str(result.content)
    match = re.search(r"channels-browse-content-grid", content, re.DOTALL)
    content = content[match.span()[1]:]

    # Find and create output for first 3 videos
    count = 0
    thumbnail_matches = r"(<img.*?width=\"288\"  >)"
    link_matches = r"(<a class=\"yt-uix-sessionlink yt-uix-tile-link.*?</a>)"
    while True:
      match = re.search(r"%s.*?%s.*" % (thumbnail_matches, link_matches), content, re.DOTALL)
      if not match or count == 3:
        break
      count += 1
      output += match.group(1) + '<br>' + match.group(2) + '<br><br><br>'

      # Strip the top off the youtube page output
      tag_end = match.span(2)[1]
      content = content[tag_end:]
    return(output)
  return("No videos found")


def twitter_list():
  
  # Fetch your Twitter page
  url = "https://twitter.com/SchibleyJ"
  result = urlfetch.fetch(url)

  # If fetch was successful
  if result.status_code == 200:
    output = ''
    content = str(result.content)

    # Find and create output for first 3 tweets
    count = 0
    tweet_matches = r"(<p class=\"ProfileTweet-text.*?</p>)"
    while True:
      match = re.search("%s.*" % tweet_matches, content, re.DOTALL)
      if not match or count == 3:
        break
      count += 1
      output += match.group(1) + '<br>'

      # Remove what we found from twitter page output
      tag_end = match.span(1)[1]
      content = content[tag_end:]
    return(output)
  return("No tweets found")