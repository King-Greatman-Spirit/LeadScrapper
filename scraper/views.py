from django.shortcuts import render
from .utils import BusinessList

def scrape_view(request):
    # Check if the request method is POST (submitted form)
    if request.method == 'POST':
        # Get the 'location' and 'sector' inputs from the submitted form
        location = request.POST.get('location')
        sector = request.POST.get('sector')
        amount = request.POST.get('amount')  # Get the specified amount from the form

        # Create an instance of the BusinessList class
        business_list = BusinessList()

        # Call the 'scrape_website' method of the BusinessList instance to scrape the website and extract business details
        businesses = business_list.scrape_website(location, sector, amount=amount)

        # Call the 'save_to_csv' method of the BusinessList instance to save the scraped data to a CSV file with serial numbers
        business_list.save_to_csv(businesses)

        # Check if there are no scraped businesses
        if not businesses:
            # Redirect to a page or display a message indicating no more unscrapped data
            return render(request, 'includes/no_data.html')

        # Check if the specified amount is greater than the number of scraped businesses
        if amount and int(amount) > len(businesses):
            # If the specified amount is greater, display the "more data" template
            return render(request, 'includes/more_data.html', {'num_scraped': len(businesses)})

        # Display the scraped data in the terminal (optional)
        for business in businesses:
            print("S/N:", business['S/N'])
            print("Business Name:", business['Business Name'])
            print("Address:", business['Address'])
            print("Phone Numbers:", business['Phone Numbers'])
            print("Email Address:", business['Email Address'])
            print("Website URL:", business['Website URL'])
            print("Social URL:", business['Social URL'])
            print("------------------------")

        # Redirect to the success page or display a success message
        return render(request, 'includes/success.html', {'num_scraped': len(businesses)})

    # Render the template for the input form if the request method is not POST
    return render(request, 'scrape/scrape_form.html')
