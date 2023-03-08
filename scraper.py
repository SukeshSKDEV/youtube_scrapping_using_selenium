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


if __name__ == "__main__":
  print('Creating driver')
  driver = get_driver()

  print('Fetching Trending videos')
  videos = get_videos(driver)

  print(f"found {len(videos)} videos")

  # title, url, thumbnail, channel,views, uploaded, description
  video = videos[0]

  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  print('Title : ', title)

  url = title_tag.get_attribute('href')
  print('URL : ', url)

  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')
  print('Thumbnail URL : ', thumbnail_url)

  channel_tag = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel = channel_tag.text
  print('Channel Name : ', channel)

  view_tag = video.find_element(
    By.XPATH,
    './/span[@class = "inline-metadata-item style-scope ytd-video-meta-block"]'
  )
  view = view_tag.text
  print(view)
