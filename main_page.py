import re
from server_scripts import *

def main_page(url):

  # Our 'root' directory is pages/.
  # This is where we keep all our web files
  path = 'pages/' + url

  # If the path ends in / then no file name was given
  # Use index.html as the default file name if not given
  if path[-1:] == '/':
    file_name = path + 'index.html'
  else:
    file_name = path

  # Try to open the file and return contents
  # If anything goes wrong return an error message instead  
  try:
    f = open(file_name, 'r')
    output = f.read()
    f.close()
  except:
    output = '<html><body>No file associated with URL %s</body></html>' % file_name

  # Find and any server side include tags
  while True:
    match = re.search(r"<!--#.*?-->", output)
    if not match:
      break
    script_name = match.group()[5:-3].strip()
    tag_start = match.span()[0]
    tag_end = match.span()[1]
    script_output = ""

    # Execute code associated with any known service side script tags    
    if script_name == 'current_time':
      script_output = current_time()

    if script_name == 'youtube_list':
      script_output = youtube_list()

    if script_name == 'twitter_list':
      script_output = twitter_list()


    # Substitute output of server side script back into page
    output = output[:tag_start] + script_output + output[tag_end:]

  return(output)






