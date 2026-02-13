import sys
import argparse
import requests
from bs4 import BeautifulSoup
import re

def get_time(location):
    """
    Scrapes time.is for the current time using requests + BeautifulSoup.
    """
    loc_path = location.replace(' ', '_')
    url = f"https://time.is/{loc_path}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # time.is typically puts the time in a div with id="twd" or id="clock"
        clock_div = soup.find(id='twd')
        if not clock_div:
            clock_div = soup.find(id='clock')
            
        if not clock_div:
            return {"error": f"Could not find clock on page for: {location}. Valid location?"}
        
        current_time = clock_div.get_text().strip()
        
        # Get date/details
        date_div = soup.find(id='dd')
        date_str = date_div.get_text().strip() if date_div else ""
        
        # Get timezone info if available
        msg_div = soup.find(id='msgdiv')
        details = msg_div.get_text().strip() if msg_div else ""

        return {
            "location": location,
            "time": current_time,
            "date": date_str,
            "details": details,
            "url": url
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check time for a location via time.is")
    parser.add_argument("location", help="Location to check (e.g., 'London', 'New York', 'Jakarta')")
    args = parser.parse_args()
    
    res = get_time(args.location)
    
    if "error" in res:
        print(f"Error: {res['error']}")
        sys.exit(1)
    else:
        print(f"Location: {res['location']}")
        print(f"Time:     {res['time']}")
        print(f"Date:     {res['date']}")
        if res['details']:
            print(f"Details:  {res['details']}")
        print(f"Source:   {res['url']}")
