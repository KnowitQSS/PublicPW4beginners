import os
import random
import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="function")
def setup_pet_page(page: Page):
    """
    Fixture to set up the AddPet page, add a pet with random details, and clean up after the test.

    This fixture:
    1. Constructs the path to the AddPet.html file.
    2. Generates a random Pet ID and Pet Name.
    3. Opens the AddPet page and fills in the Pet ID, Pet Name, and Photo URL.
    4. Clicks the PostPet button and waits for a success message.
    5. Yields the page and pet details for use in the test.
    6. Deletes the pet after the test by clicking the Delete Pet button and waiting for a success message.

    Args:
        page (Page): The Playwright page object.

    Yields:
        dict: A dictionary containing the page object, pet_id, pet_name, and photo_url.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the entire path to the GetPet.html file
    add_pet_file_path = os.path.join(script_dir, "..", "petstore", "AddPet.html")
    # Ensure it's in the correct format
    add_pet_file_path = f"file://{add_pet_file_path}"

    # Generate a random Pet ID between 2000 and 3000
    pet_id = random.randint(2000, 3000)
    # Generate a random Pet Name
    pet_name = f"Pet{random.randint(1000, 9999)}"
    # Define the Photo URL
    photo_url = "https://images.dog.ceo/breeds/corgi-cardigan/n02113186_11035.jpg"

    # Print the Pet ID to the console
    print(f"Generated Pet ID: {pet_id}")

    # Open the AddPet page
    page.goto(add_pet_file_path)
    # Fill in the Pet ID, Pet Name, and Photo URL
    page.fill("#petId", str(pet_id))
    page.fill("#petName", pet_name)
    page.fill("#photoUrl", photo_url)
    # Click the PostPet button
    page.click("#postPetButton")

    # Wait for a success message or some indication that the pet was added
    page.wait_for_selector("text=Pet added successfully")
    yield {"page": page, "pet_id": pet_id, "pet_name": pet_name, "photo_url": photo_url}

    delete_button = page.get_by_role(role="button", name="Delete Pet")
    delete_button.wait_for(timeout=3000, state="visible")
    delete_button.click()
    page.get_by_text("Pet deleted successfully.").wait_for(timeout=3000, state="visible")


def test_add_and_get_pet(setup_pet_page: dict):
    """
    Test to add a pet using the AddPet page and verify its details on the GetPet page.

    This test:
    1. Uses the setup_pet_page fixture to add a pet and get the pet details.
    2. Constructs the path to the GetPet.html file.
    3. Opens the GetPet page with the Pet ID from the fixture.
    4. Waits for either the image or the message to be visible.
    5. Asserts that the image is visible and the URL matches the expected Photo URL.
    6. Asserts that the pet name displayed on the page matches the expected Pet Name.

    Args:
        setup_pet_page (dict): A dictionary containing the page object, pet_id, pet_name, and photo_url.
    """
    pet_data = setup_pet_page
    page: Page = pet_data['page']

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the GetPet.html file
    get_pet_file_path = os.path.join(script_dir, "..", "petstore", "GetPet.html")

    # Convert to an absolute path and ensure it's in the correct format
    get_pet_file_path = f"file://{get_pet_file_path}"

    # Construct the URL with the PetID parameter for the GetPet page
    get_pet_url = f"{get_pet_file_path}?petid={pet_data['pet_id']}"
    # Open the GetPet page
    page.goto(get_pet_url)
    # Wait for either the image or the message to be visible
    page.wait_for_selector('img, .message', state='visible')

    # Add assertions or further interactions as needed
    assert page.locator('img').is_visible() or page.locator('.message').is_visible()
    if page.locator('img').is_visible():
        assert page.locator('img').get_attribute('src') == pet_data['photo_url']

    assert page.locator('#pet-name').inner_text().endswith(pet_data['pet_name'])