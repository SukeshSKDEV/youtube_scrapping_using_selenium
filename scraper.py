import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_TRENDING_VIDEOS = 'https://www.youtube.com/feed/trending'


def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver


def get_videos(driver):
  driver.get(YOUTUBE_TRENDING_VIDEOS)
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos


def parse_video(video):

  # title, url, thumbnail, channel,views, uploaded, description

  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text

  url = title_tag.get_attribute('href')

  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')

  channel_tag = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel = channel_tag.text

  view_tags = video.find_element(By.XPATH, '//*[@id="metadata-line"]/span[1]')
  view = view_tags.text

  uploaded_tag = video.find_element(By.XPATH,
                                    '//*[@id="metadata-line"]/span[2]')
  uploaded = uploaded_tag.text

  desc_tag = video.find_element(By.ID, 'description-text')
  desc = desc_tag.text

  return {
    'title': title,
    'url': url,
    'thumbnail_url': thumbnail_url,
    'channel': channel,
    'description': desc,
    'view': view,
    'uploaded': uploaded
  }


if __name__ == "__main__":
  print('Creating driver')
  driver = get_driver()

  print('Fetching Trending videos')
  videos = get_videos(driver)

  print(f"found {len(videos)} videos")

  print("Parsing top 10 trending videos")
  videos_data = [parse_video(video) for video in videos[:10]]

  print("Save the data to CSV file")
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)

  videos_df.to_csv('trending.csv', index=None)
