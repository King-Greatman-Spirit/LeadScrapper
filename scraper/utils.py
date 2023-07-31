import re
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

class BusinessList:
    # Function to remove special characters, replace spaces with hyphens, and convert text to lowercase
    def sanitize_input(self, text):
        remove_chars = [",", "!", ".", "@", "#", "&", "^", "(", ")", "\""]
        text = ''.join(char for char in text if char not in remove_chars)
        text = text.replace(" ", "-").lower()
        return text.strip()

    # Function to extract the website URL from the details_soup
    def extract_website(self, details_soup):
        # Check if the website element exists in the details_soup
        website_element = details_soup.select_one(".cmp_details .info .text.weblinks a")
        if website_element:
            return website_element.text.strip()
        else:
            # If the website element is not found, extract the website URL from the description text using regex
            description_element = details_soup.select_one(".info .text.desc")
            if description_element:
                description_text = description_element.text.strip()
                website_matches = re.findall(r"(https?://[\w.-]+\.[a-zA-Z]{2,})", description_text)
                if website_matches:
                    return website_matches[0]
        return None

    # Function to check if the website URL is valid and starts with "https"
    def is_valid_https_website(self, url):
        pattern = r"^https://[\w.-]+\.[a-zA-Z]{2,}"
        return bool(re.match(pattern, url))

    # Function to check if the URL is a social media link
    def is_social_media_link(self, url):
        social_media_domains = [
            r"(?:www\.)?facebook\.com",
            r"(?:www\.)?twitter\.com",
            r"(?:www\.)?instagram\.com",
            r"(?:www\.)?linkedin\.com",
            r"(?:chat\.)?whatsapp\.com",
            # Add more social media domains as needed
        ]
        social_media_pattern = "|".join(social_media_domains)
        return bool(re.search(social_media_pattern, url, re.IGNORECASE))

    # Function to scrape the website and extract business details
    def scrape_website(self, city, category):
        # Sanitize the user inputs for city and category
        city = self.sanitize_input(city)
        category = self.sanitize_input(category)

        # Construct the URL for the main page of the specified city and category
        main_url = f"https://www.businesslist.com.ng/category/{category}/city:{city}"
        print("Main URL:", main_url)

        # Send a request to the main page and parse the HTML content using BeautifulSoup
        main_response = requests.get(main_url)
        main_soup = BeautifulSoup(main_response.text, "html.parser")

        businesses = []

        # Loop through the business elements on the main page
        for idx, business_element in enumerate(main_soup.select(".company.with_img.g_0"), start=1):
            # Extract business name and address from the business element
            business_name = business_element.select_one("h4 a")['title']
            address = business_element.select_one(".address").text.strip()

            # Extract the details link from the business element and form the full URL
            details_link_element = business_element.select_one("h4 a")
            if details_link_element:
                details_link = details_link_element['href']
                details_url = f"https://www.businesslist.com.ng{details_link}"
                details_response = requests.get(details_url)

                # Parse the details page using BeautifulSoup
                details_soup = BeautifulSoup(details_response.text, "html.parser")

                # Extract phone numbers from the details page
                phone_elements = details_soup.select(".info .text.phone, .info .text:not(.phone)")
                phone_numbers = []
                scraped_numbers = set()  # Set to store already scraped numbers

                for phone_element in phone_elements:
                    phone_number = re.sub(r"[^0-9+]", "", phone_element.text.strip())
                    if phone_number and 11 <= len(phone_number) <= 14:
                        phone_numbers.append(phone_number)
                        scraped_numbers.add(phone_number)

                if not phone_numbers:
                    phone_numbers = ["No Phone Number Found"]

                # Extract email addresses from the details page
                email_addresses = []
                scraped_emails = set()  # Set to store already scraped email addresses

                description_element = details_soup.select_one(".info .text.desc")
                if description_element:
                    description_text = description_element.text.strip()
                    email_matches = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", description_text)
                    for match in email_matches:
                        if match not in scraped_emails:
                            email_addresses.append(match)
                            scraped_emails.add(match)

                if not email_addresses:
                    email_addresses = ["No Email Address Found"]

                # Extract the website URL from the details page using the extract_website method
                website = self.extract_website(details_soup)
                if not website:
                    website = "No Website URL"

                # Construct the business data dictionary
                business_data = {
                    'S/N': idx,
                    'Business Name': business_name,
                    'Address': address,
                    'Phone Numbers': phone_numbers,
                    'Email Address': ", ".join(email_addresses),
                    'Website URL': website,
                    'Social URL': '',  # Initialize the social_url to empty
                }

                # Additional check for social media link
                if self.is_social_media_link(website):
                    business_data['Social URL'] = website
                    business_data['Website URL'] = ''

                businesses.append(business_data)

        return businesses

    # Function to save the scraped results to a CSV file
    def save_to_csv(self, results):
        with open('scraped_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['S/N', 'Business Name', 'Address', 'Phone Numbers', 'Email Address', 'Website URL', 'Social URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')  # Use tab ("\t") as the delimiter
            writer.writeheader()

            # Add a serial number to each row and then write them to the CSV file
            for idx, result in enumerate(results, start=1):
                result_with_serial = {'S/N': idx, **result}
                writer.writerow(result_with_serial)
