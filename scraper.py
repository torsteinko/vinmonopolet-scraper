import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

def load_stores():
    """Loads stores from the CSV file created by the first script."""
    filename = 'stores_list.csv'
    if not os.path.exists(filename):
        print(f"Error: '{filename}' missing. Please run 'extract_stores.py' first.")
        return []
    return pd.read_csv(filename).to_dict('records')

def scrape_vinmonopolet(store_id, store_name, wine_type_code, wine_label):
    """Main scraping logic."""
    
    # Construct URL
    url = f"https://www.vinmonopolet.no/search?q=%3Arelevance%3AavailableInStores%3A{store_id}%3AmainCategory%3A{wine_type_code}"
    
    # Create safe filename (e.g., vinmonopolet_Bergen_Sletten_white_wines.csv)
    safe_name = store_name.replace(', ', '_').replace(' ', '_').replace('/', '-')
    output_file = f"vinmonopolet_{safe_name}_{wine_label}.csv"

    print(f"\n--- STARTING SCRAPE ---")
    print(f"Target: {store_name}")
    print(f"Type:   {wine_label.replace('_', ' ').title()}")
    print(f"File:   {output_file}")
    
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # If someone wants to run this headless it's possible.
    driver = webdriver.Chrome(options=options)
    
    all_wines = []
    page_num = 1

    try:
        driver.get(url)

        # Cookie Consent
        try:
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Godkjenn alle')]"))).click()
            time.sleep(0.5)
        except TimeoutException: pass
        
        # Age Gate
        try:
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ja, jeg er over 18 år')]"))).click()
            time.sleep(0.5)
        except TimeoutException: pass

        # Loop pages
        while True:
            print(f"Scraping page {page_num}...")
            
            wait = WebDriverWait(driver, 10)
            try:
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.product-item')))
            except TimeoutException:
                print("Timed out waiting for products.")
                break

            time.sleep(1.5) # Buffer for content load

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            items = soup.find_all('li', class_='product-item')

            for item in items:
                name_tag = item.find('div', class_='product__name')
                price_tag = item.find('span', class_='product__price')

                if name_tag and price_tag:
                    name = name_tag.text.strip()
                    # Clean price: remove 'Kr', spaces, fix decimal
                    p_text = price_tag.text.strip().replace('Kr', '').replace('\xa0', '').replace(' ', '').replace(',', '.')
                    try:
                        price = float(p_text)
                        all_wines.append({'name': name, 'price': price})
                    except ValueError:
                        continue
            
            # Next Page
            try:
                next_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Gå til neste side"]')
                if "disabled" in next_btn.get_attribute("class"):
                    break
                driver.execute_script("arguments[0].click();", next_btn)
                page_num += 1
                time.sleep(2)
            except NoSuchElementException:
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    # Save
    if all_wines:
        df = pd.DataFrame(all_wines)
        df = df.sort_values(by='price', ascending=False)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\nDone! Saved {len(all_wines)} wines to '{output_file}'")
    else:
        print("\nNo wines found.")

if __name__ == '__main__':
    stores = load_stores()
    
    if stores:
        print(f"Loaded {len(stores)} stores.")
        
        # Store Selection
        while True:
            search = input("Search for store (or press Enter to see all): ").lower().strip()
            
            # Filter stores based on search
            filtered = [s for s in stores if search in s['name'].lower()]
            
            if not filtered:
                print("No matches found.")
                continue

            # Display options
            print("\n--- Stores ---")
            for i, store in enumerate(filtered, 1):
                print(f"{i}. {store['name']}")
            
            try:
                sel = int(input("\nSelect number (or 0 to search again): "))
                if sel == 0: continue
                if 1 <= sel <= len(filtered):
                    selected_store = filtered[sel - 1]
                    break
            except ValueError:
                pass
        
        # Wine Type Selection
        print(f"\nSelected: {selected_store['name']}")
        print("1: Red Wines")
        print("2: White Wines")
        
        while True:
            choice = input("Choice: ").strip()
            if choice == '1':
                scrape_vinmonopolet(selected_store['id'], selected_store['name'], "r%C3%B8dvin", "red_wines")
                break
            elif choice == '2':
                scrape_vinmonopolet(selected_store['id'], selected_store['name'], "hvitvin", "white_wines")
                break
