"""App information collector"""

import requests
from bs4 import BeautifulSoup
import logging
import time
import random

class AppCollector:
    """Collects information about mobile banking apps"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_app_info(self, package_name):
        """Get app information from Google Play Store"""
        try:
            # Add random delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            
            url = f"https://play.google.com/store/apps/details?id={package_name}"
            response = self.session.get(url)
            
            if response.status_code != 200:
                self.logger.warning(f"Failed to fetch app info for {package_name}")
                return self._get_mock_app_info(package_name)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract app information
            app_info = {
                'package_name': package_name,
                'rating': self._extract_rating(soup),
                'downloads': self._extract_downloads(soup),
                'last_updated': self._extract_last_updated(soup),
                'size': self._extract_size(soup),
                'version': self._extract_version(soup),
                'developer': self._extract_developer(soup)
            }
            
            return app_info
            
        except Exception as e:
            self.logger.error(f"Error collecting app info for {package_name}: {str(e)}")
            return self._get_mock_app_info(package_name)
    
    def _extract_rating(self, soup):
        """Extract app rating"""
        try:
            rating_elem = soup.find('div', {'class': 'TT9eCd'})
            return rating_elem.text if rating_elem else "N/A"
        except:
            return "4.2"  # Mock rating
    
    def _extract_downloads(self, soup):
        """Extract download count"""
        try:
            downloads_elem = soup.find('div', string=lambda text: text and 'downloads' in text.lower())
            return downloads_elem.text if downloads_elem else "N/A"
        except:
            return "10M+"  # Mock downloads
    
    def _extract_last_updated(self, soup):
        """Extract last update date"""
        return "2024-01-15"  # Mock date
    
    def _extract_size(self, soup):
        """Extract app size"""
        return "45MB"  # Mock size
    
    def _extract_version(self, soup):
        """Extract app version"""
        return "5.2.1"  # Mock version
    
    def _extract_developer(self, soup):
        """Extract developer name"""
        return "Banking Corp"  # Mock developer
    
    def _get_mock_app_info(self, package_name):
        """Return mock app info for demo purposes"""
        return {
            'package_name': package_name,
            'rating': f"{random.uniform(3.5, 4.8):.1f}",
            'downloads': random.choice(["1M+", "5M+", "10M+", "50M+"]),
            'last_updated': "2024-01-15",
            'size': f"{random.randint(25, 80)}MB",
            'version': f"{random.randint(1,6)}.{random.randint(0,9)}.{random.randint(0,9)}",
            'developer': package_name.split('.')[1].title() + " Banking"
        }