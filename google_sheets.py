import gspread
from google.oauth2.service_account import Credentials
import logging
from datetime import datetime
from config import GOOGLE_SHEETS_CREDENTIALS_FILE, GOOGLE_SHEET_ID

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleSheetsManager:
    def __init__(self):
        self.sheet = None
        self.worksheet = None
        self._connect_to_sheets()
    
    def _connect_to_sheets(self):
        """Connect to Google Sheets using service account credentials"""
        try:
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Load credentials
            creds = Credentials.from_service_account_file(
                GOOGLE_SHEETS_CREDENTIALS_FILE, 
                scopes=scope
            )
            
            # Authorize and open the sheet
            gc = gspread.authorize(creds)
            self.sheet = gc.open_by_key(GOOGLE_SHEET_ID)
            self.worksheet = self.sheet.sheet1
            
            # Set up headers if the sheet is empty
            if not self.worksheet.get_all_records():
                self._setup_headers()
                
            logger.info("Successfully connected to Google Sheets")
            
        except Exception as e:
            logger.error(f"Error connecting to Google Sheets: {e}")
            raise
    
    def _setup_headers(self):
        """Set up column headers in the sheet"""
        headers = [
            'ID', 'Username', 'First Name', 'Last Name', 
            'Telegram ID', 'Phone', 'Registration Date', 'Last Activity'
        ]
        self.worksheet.append_row(headers)
        logger.info("Headers set up in Google Sheets")
    
    def add_user(self, user_data):
        """Add a new user to the Google Sheet"""
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Get the next ID
            records = self.worksheet.get_all_records()
            next_id = len(records) + 1
            
            # Prepare user data
            row_data = [
                next_id,
                user_data.get('username', ''),
                user_data.get('first_name', ''),
                user_data.get('last_name', ''),
                user_data.get('telegram_id', ''),
                user_data.get('phone', ''),
                current_time,
                current_time
            ]
            
            # Add the row
            self.worksheet.append_row(row_data)
            logger.info(f"User {user_data.get('username', 'Unknown')} added to Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Error adding user to Google Sheets: {e}")
            return False
    
    def update_user_activity(self, telegram_id):
        """Update user's last activity timestamp"""
        try:
            records = self.worksheet.get_all_records()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            for i, record in enumerate(records, start=2):  # Start from row 2 (skip header)
                if str(record.get('Telegram ID', '')) == str(telegram_id):
                    self.worksheet.update_cell(i, 8, current_time)  # Column 8 is 'Last Activity'
                    break
                    
        except Exception as e:
            logger.error(f"Error updating user activity: {e}")
    
    def get_all_users(self):
        """Get all users from the sheet"""
        try:
            records = self.worksheet.get_all_records()
            return records
        except Exception as e:
            logger.error(f"Error getting users from Google Sheets: {e}")
            return []
    
    def get_user_count(self):
        """Get total number of users"""
        try:
            records = self.worksheet.get_all_records()
            return len(records)
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0
