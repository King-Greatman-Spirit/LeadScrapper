from django.test import TestCase

# Create your tests here.

# from bs4 import BeautifulSoup
# import requests

# def sanitize_input(text):
#     # Define characters to remove
#     remove_chars = [",", "!", ".", "@", "#", "&", "^", "(", ")", "\""]

#     # Remove specified characters
#     text = ''.join(char for char in text if char not in remove_chars)

#     # Replace spaces with dashes and convert input to lowercase
#     text = text.replace(" ", "-").lower()

#     return text.strip()

# def scrape_website(city, category):
#     city = sanitize_input(city)
#     category = sanitize_input(category)

#     url = f"https://www.businesslist.com.ng/category/{category}/city:{city}"
#     print("URL:", url)  # Print statement for URL construction
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")

#     businesses = []

#     for idx, business_element in enumerate(soup.select(".company.with_img.g_0"), start=1):
#         business_name = business_element.select_one(".cmp_details #company_name").text.strip()
#         address = business_element.select_one(".cmp_details .text.location").text.strip()

#         details_link_element = business_element.select_one(".cmp_details_in .cmp_details .info .text.weblinks a")
#         print("Detail link element worked!")
         
#         if details_link_element:
#             print("if statement worked")
#             details_link = details_link_element['href']
#             print("Details link!")
#             details_url = f"https://www.businesslist.com.ng/{details_link}"
#             print("Details URL:", details_url)  # Print statement for details URL
#             details_response = requests.get(details_url)
#             print("Details Response!")
            
#             details_soup = BeautifulSoup(details_response.text, "html.parser")
#             print("Detail Soup")
#             print("Details Response:", details_response)
#             print("Detail Response!!!")

#             phone_numbers = [phone.text.strip() for phone in details_soup.select(".cmp_details .info .text.phone")]
#             email = details_soup.select_one(".cmp_details .info .text a[href^='/company/']")
#             if email:
#                 email = email.text.strip()
#             else:
#                 email = ""
                
#             website = details_soup.select_one(".cmp_details .info .text.weblinks a")
#             if website:
#                 website = website['href']
#             else:
#                 website = ""
#         else:
#             phone_numbers = []
#             email = ""
#             website = ""

#         business = {
#             'name': business_name,
#             'address': address,
#             'phone_numbers': phone_numbers,
#             'email': email,
#             'website': website
#         }
#         businesses.append(business)

#     return businesses

# # Example usage
# city = input("Enter the city: ")
# category = input("Enter the category: ")
# results = scrape_website(city, category)

# for idx, result in enumerate(results, start=1):
#     print("S/n:", idx)
#     print("Business name:", result['name'])
#     print("Address:", result['address'])
#     print("Phone Numbers:", ", ".join(result['phone_numbers']))
#     print("Email:", result['email'])
#     print("Website:", result['website'])
#     print("------------------------")
