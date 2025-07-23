from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Tuple
from datetime import datetime
from app.models.event import format_date

class EventParser:
    def __init__(self, url: str):
        self.url = url

    def extract_title(self, soup: BeautifulSoup) -> str:
        """
        Extracts the event title from the soup.
        """
        # Updated selector to match <span class="paragraph event-title">
        title_tag = soup.find('span', class_='event-title')
        return title_tag.get_text(strip=True) if title_tag else ''

    def extract_description(self, soup: BeautifulSoup) -> str:
        """
        Extracts the event description from the soup.
        Returns a string with compacted newlines.
        """
        desc_tag = soup.find('p', class_='information-description')
        if desc_tag:
            description = desc_tag.get_text(separator='\n', strip=True)
            description = re.sub(r'\n+', '\n', description).strip()
            return description
        return ''

    def extract_brackets(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        Extracts the list of brackets from the soup.
        Each bracket is a dict with 'name' and 'format'.
        """
        brackets = []
        battles_section = soup.find('div', class_='battles')
        if battles_section:
            for battle in battles_section.find_all('a', class_='battle-chip'):
                bracket_name = battle.find('p', class_='title')
                bracket_format = battle.find('span', class_='type')
                brackets.append({
                    'name': bracket_name.get_text(strip=True) if bracket_name else '',
                    'format': bracket_format.get_text(strip=True) if bracket_format else ''
                })
        return brackets

    def extract_location(self, soup: BeautifulSoup) -> str:
        """
        Extracts the event location from the soup by finding the location icon
        and the neighboring <a> tag in the same <p>.
        """
        location_icon_path = "M12,2C15.31,2 18,4.66 18,7.95C18,12.41 12,19 12,19C12,19 6,12.41 6,7.95C6,4.66 8.69,2 12,2M12,6A2,2 0 0,0 10,8A2,2 0 0,0 12,10A2,2 0 0,0 14,8A2,2 0 0,0 12,6M20,19C20,21.21 16.42,23 12,23C7.58,23 4,21.21 4,19C4,17.71 5.22,16.56 7.11,15.83L7.75,16.74C6.67,17.19 6,17.81 6,18.5C6,19.88 8.69,21 12,21C15.31,21 18,19.88 18,18.5C18,17.81 17.33,17.19 16.25,16.74L16.89,15.83C18.78,16.56 20,17.71 20,19Z"
        for p in soup.find_all('p', class_='paragraph'):
            span = p.find('span', class_='v-icon notranslate icon theme--light')
            if span:
                svg = span.find('svg')
                if svg and svg.find('path') and svg.find('path').get('d') == location_icon_path:
                    a_tag = p.find('a', href=True)
                    if a_tag:
                        return a_tag.get_text(strip=True)
        return ''

    def _format_date(self, date_str: str) -> str:
        """
        Converts a date string like 'January 5th, 2025' to 'MM/DD/YYYY' with leading zeros.
        Returns the original string if parsing fails.
        """
        if not date_str:
            return ""
        # Remove ordinal suffixes (st, nd, rd, th)
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
        try:
            dt = datetime.strptime(date_str.strip(), "%B %d, %Y")
            return dt.strftime("%m/%d/%Y")
        except Exception:
            return date_str

    def extract_dates(self, soup: BeautifulSoup) -> Tuple[str, str]:
        """
        Extracts the start and end dates from the soup by finding the calendar icon
        and parsing the text next to it.
        Returns a tuple (start_date, end_date) in MM/DD/YYYY format.
        """
        start_date = ''
        end_date = ''

        calendar_icon = soup.find('span', class_='v-icon notranslate icon theme--light')
        if calendar_icon and calendar_icon.next_sibling:
            next_elem = calendar_icon.next_sibling
            if hasattr(next_elem, 'get_text'):
                date_text = next_elem.get_text(strip=True)
            else:
                date_text = str(next_elem).strip()
            if '-' in date_text:
                parts = [p.strip() for p in date_text.split('-')]
                start_date = format_date(parts[0])
                end_date = format_date(parts[1]) if len(parts) > 1 else format_date(parts[0])
            else:
                start_date = format_date(date_text)
                end_date = format_date(date_text)
        return start_date, end_date

    def extract_times(self, soup: BeautifulSoup) -> Tuple[str, str]:
        """
        Extracts the start and end times from the soup by finding the clock icon
        and parsing the text next to it.
        Returns a tuple (start_time, end_time).
        """
        start_time = ''
        end_time = ''
        
        # Use SVG icon path to identify clock icon. Time text should be it's neighbor.
        clock_icon_path = "M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z"
        for span in soup.find_all('span', class_='v-icon notranslate icon theme--light'):
            svg = span.find('svg')
            if svg and svg.find('path') and svg.find('path').get('d') == clock_icon_path:
                parent = span.parent
                if parent and parent.text:
                    time_text = parent.get_text(separator=' ', strip=True)
                    if '-' in time_text:
                        parts = [p.strip() for p in time_text.split('-')]
                        start_time = parts[0]
                        end_time = parts[1] if len(parts) > 1 else parts[0]
                    else:
                        start_time = time_text
                        end_time = time_text
                break
        return start_time, end_time

    def fetch_event_details(self) -> dict:
        """
        Uses Selenium to load the event page, parses it with BeautifulSoup,
        and extracts all event details using helper methods.
        Returns a dictionary with all event fields.
        """
        # Load page w/ Selenium, headless mode disabled due to issues with the event page rendering
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        # Wait for the event content to load. The wait is necessary to extract data from the rendered html
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "event-title"))
            )
        except Exception:
            driver.quit()
            raise Exception("Event content did not load in time.")

        html = driver.page_source
        driver.quit()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        title = self.extract_title(soup)
        description = self.extract_description(soup)
        brackets = self.extract_brackets(soup)
        location = self.extract_location(soup)
        start_date, end_date = self.extract_dates(soup)
        start_time, end_time = self.extract_times(soup)

        event_link = self.url

        return {
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            'start_time': start_time,
            'end_time': end_time,
            'location': location,
            'event_link': event_link,
            'brackets': brackets,
            'description': description
        }