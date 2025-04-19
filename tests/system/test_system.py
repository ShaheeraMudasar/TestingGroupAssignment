from playwright.sync_api import sync_playwright, expect, Page


# Test case: When the user visits 'visits' page it return the history of visits (Tester: Shaheera)
def test_visits_display_all_visits(page):
    # GIVEN a user opens the visits page
    # WHEN the user opens vists page
    page.goto("http://127.0.0.1:5000/visits")

    # THEN the page should show json containing visits history
    visit_data = page.locator("body")
    expect(visit_data).to_contain_text("user_agent")
    expect(visit_data).to_contain_text("timestamp")

# Test case: When the user visits 'visits/<id>' page it return visit detail of that visit id 
def test_visit_by_id_should_return_visit_detail_of_that_visit_id(page):
    # GIVEN the user opens the visit page
    # WHEN the user enters a visit id 1

    page.goto("http://127.0.0.1:5000/visit/1")

    # THEN it should return the visit details of visit id 1
    visit_detail = page.locator("body")
    expect(visit_detail).to_contain_text("When")
    expect(visit_detail).to_contain_text("IP")
    expect(visit_detail).to_contain_text("User agent")

