from django.shortcuts import render
from .utils import BusinessList

def scrape_view(request):
    # Check if the request method is POST (submitted form)
    if request.method == 'POST':
        # Get the 'location' and 'sector' inputs from the submitted form
        location = request.POST.get('location')
        sector = request.POST.get('sector')

        # Create an instance of the BusinessList class
        business_list = BusinessList()

        # Call the 'scrape_website' method of the BusinessList instance to scrape the website and extract business details
        businesses = business_list.scrape_website(location, sector)

        # Call the 'save_to_csv' method of the BusinessList instance to save the scraped data to a CSV file with serial numbers
        business_list.save_to_csv(businesses)

        # Display the scraped data in the terminal (optional)
        # for business in businesses:
        #     print("S/N:", business['S/N'])
        #     print("Business Name:", business['Business Name'])
        #     print("Address:", business['Address'])
        #     print("Phone Numbers:", business['Phone Numbers'])
        #     print("Email Address:", business['Email Address'])  # Use 'Email Address' instead of 'email'
        #     print("Website URL:", business['Website URL'])
        #     print("Social URL:", business['Social URL'])
            # print("------------------------")

        # Redirect to a success page or display a success message
        return render(request, 'includes/success.html')

    # Render the template for the input form if the request method is not POST
    return render(request, 'scrape/scrape_form.html')
