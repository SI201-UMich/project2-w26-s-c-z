# SI 201 HW4 (Library Checkout System)
# Your name: Clare Mathison, Sofia Ayala
# Your student id: 7537 9681, 0309 8022
# Your email: claremat@umich.edu, ayasofia@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): Sofia Ayala and Zuza Harris
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    
    html_file = html_path
    with open(html_file, 'r', encoding="utf-8-sig") as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
    lst = []
    listings = soup.find_all('div', class_ = 't1jojoys')
    for i in range(len(listings)):
        listing = ' '.join(listings[i].text.split())
        id = listings[i].get('id')[6:]
        lst.append((listing, id))
    return lst


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    
    html_file = os.path.join("html_files", f"listing_{listing_id}.html")
    with open(html_file, 'r', encoding="utf-8-sig") as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
    ans_d = {}
    inner_d ={}
    ans_d[listing_id] = inner_d

    host = soup.find('div', class_ = '_1k8vduze')
    policy_num = host.find('span', class_ = 'll4r2nl').text
    if policy_num:
        inner_d['policy_number'] = policy_num
    
    host_type = soup.find('span', class_ = "_1mhorg9")
    if host_type:
        inner_d['host_type'] = "Superhost"
    else:
        inner_d['host_type'] = 'regular'

    host_tag = soup.find('div', class_ = 'c6y5den')
    host = host_tag.find('h2', class_ = 'hnwb2pb').text
    inner_d['host_name'] = host.strip()[10:]

    room_tag = soup.find('div', class_ = '_cv5qq4')
    room_type = room_tag.find('h2', class_ = '_14i3z6h').text
    if 'private' in room_type.lower():
        inner_d['room_type'] = 'Private'
    elif 'shared' in room_type.lower():
        inner_d['room_type'] = 'Shared'
    else:
        inner_d['room_type'] = 'Entire Room'

    ratings_tag = soup.find_all('div', class_ = '_a3qxec')
    
    rating_val = 0.0
    for tag in ratings_tag:
            
            rating = tag.find('div', class_ = '_y1ba89')
            
            if rating and rating.text.strip() == "Location":
                rating_val = tag.find('span', class_='_4oybiu').text
                
    inner_d['location_rating'] = float(rating_val)
    ans_d[listing_id] = inner_d
    print(ans_d)
    return ans_d

 


def create_listing_database(html_path) -> list[tuple]: 
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listings = load_listing_results(html_path)
    database = []

    for listing_title, listing_id in listings: 
        details = get_listing_details(listing_id)
        info = details[listing_id]

        row = (
            listing_title, 
            listing_id, 
            info["policy_number"], 
            info["host_type"], 
            info["host_name"],
            info["room_type"],
            info["location_rating"],
        )
        database.append(row)
    
    return database
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    
    # # TODO: Implement checkout logic following the instructions
    # # ==============================
    # # YOUR CODE STARTS HERE
    # # ==============================
    headers = [
        "Listing Title",
        "Listing ID",
        "Policy Number",
        "Host Type",
        "Host Name",
        "Room Type",
        "Location Rating", 
    ]

    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(sorted_data)
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    room_totals = {}

    for listing in data:
        room_type = listing[5]
        location_rating = listing[6]

        if location_rating == 0.0:
            continue
        if room_type not in room_totals:
            room_totals[room_type] = []
        room_totals[room_type].append(location_rating)

    averages = {}
    for room_type, ratings in room_totals.items():
        averages[room_type] = round(sum(ratings) / len(ratings), 1)

    return averages


    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid_ids = []
    pattern = r'^(20\d{2}-00\d{4}STR|STR-000\d{4})$'

    for listing in data:
        listing_id = listing[1]
        policy_number = listing[2]

        if policy_number in ("Pending", "Exempt"):
            continue

        if not re.match(pattern, policy_number):
            invalid_ids.append(listing_id)

    return invalid_ids
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    url = "https://scholar.google.com/scholar?q=" + query
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = []
    for result in soup.find_all("h3", class_="gs_rt"):
        titles.append(result.get_text())
        
    return titles
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")
        
        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        
        self.assertEqual(len(self.listings), 18)
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        results = []
        for id in html_list:
            results.append(get_listing_details(id))

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(results[0]["467507"]["policy_number"], "STR-0005349")
        self.assertEqual(results[2]["1944564"]["host_type"], "Superhost")
        self.assertEqual(results[2]["1944564"]["room_type"], "Entire Room")
        self.assertEqual(results[2]["1944564"]["location_rating"], 4.9)

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        for row in self.detailed_data:
            self.assertEqual(len(row), 7)
        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        self.assertEqual(self.detailed_data[-1], ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8))

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        out_path = os.path.join(self.base_dir, "test.csv")
        output_csv(self.detailed_data, out_path)

        # TODO: Read the CSV back in and store rows in a list.
        with open(out_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        self.assertEqual(rows[1], ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"])
        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        result = avg_location_rating_by_room_type(self.detailed_data)
        self.assertEqual(result["Private Room"], 4.9)

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        invalid_listings = validate_policy_numbers(self.detailed_data)
        self.assertEqual(invalid_listings, ["16204265"])


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)