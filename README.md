# Vinmonopolet Local Store Scraper 🍷

A Python tool designed to scrape the complete wine inventory (Red & White) from your local **Vinmonopolet** store.

## 🎯 The Goal
The primary purpose of this tool is to generate a clean dataset (`.csv`) of available wines in your specific local store. You can then upload this file to an AI assistant (like ChatGPT, Claude, or Gemini) to get **highly personalized wine recommendations** based on exactly what is in stock near you.

**Example Prompt for AI:**
> "Here is the list of white wines at my local store (attached csv). I'm cooking a spicy Thai curry tonight and I prefer dry wines with high acidity. My budget is under 250 NOK. Which 3 wines from this list would you recommend and why?"

## 🚀 Features
- **Store Selector**: Automatically reads a list of all Vinmonopolet stores and lets you choose yours by name/ID.
- **Live Price & Inventory**: Scrapes real-time data directly from Vinmonopolet's website.
- **Clean Output**: Generates a formatted `.csv` file ready for data analysis or AI context.
- **Polite Scraping**: Handles cookie banners and age verification gates automatically.

## 🛠️ Installation

1. **Clone the repository**
   ```
   git clone https://github.com/torsteinko/vinmonopolet-scraper.git
   cd vinmonopolet-scraper
   ```

2. **Install Dependencies** (Recommended to use a virtual environment) 
   ```
   pip install -r requirements.txt
   ```

## 📖 Usage

### Step 1: Scrape Your Local Store
Run the main scraper. It will ask you to search for your store and choose the wine type.
```
python scraper.py
```
**Interactive Steps:**
1. Type part of your store's name (e.g., "Bergen" or "Stavanger").
2. Select the store from the numbered list.
3. Choose `1` for Red Wine or `2` for White Wine.
4. Wait for the script to finish scraping.

### Step 2: Get Recommendations
1. Locate the generated file (`vinmonopolet_STORENAME_WINETYPE.csv`).
2. Upload it to your favorite AI assistant.
3. Ask for recommendations based on your meal, taste preferences, or budget!

## 📂 Files
- `scraper.py`: The main script for fetching wine data.
- `extract_stores.py`: Utility script to parse store IDs from raw HTML.
- `stores_list.csv`: Generated list of all stores and their IDs.
- `requirements.txt`: Python package dependencies.

## ⚖️ Disclaimer
This tool is for personal use only. Please respect Vinmonopolet's terms of service and avoid aggressive scraping (e.g., running it thousands of times in a short loop).

### How to add this to your repo
1. Create a new file named `README.md` in your folder.
2. Paste the text above into it.
3. Save it.
4. Run these commands in your terminal to update the repo:

```
git add README.md
git commit -m "Add README with AI recommendation use case"
git push
```
## 📝 Todo / Roadmap

### 🔍 Scraper Expansion
- [ ] **Add Beer Support**: Expand scraper to handle the Beer category (`øl`) with sub-categories (IPA, Lager, Stout).
- [ ] **Add Spirits Support**: Add support for Whiskey, Gin, and Vodka.
- [ ] **Extract More Details**: Capture additional fields beyond just name/price:
    - [ ] Vintage (Year)
    - [ ] Country / Region
    - [ ] Volume (cl) & Alcohol Content (%)
    - [ ] Link to product page

### ⚙️ Technical Improvements
- [X] **Headless Mode Toggle**: Add a simple configuration to run the browser invisibly (headless).
- [ ] **Error Handling**: Improve retry logic for slow connections or if Vinmonopolet changes their CSS selectors.
- [ ] **Auto-Update Store List**: Create a script to fetch the fresh "All Stores" HTML directly from the web instead of relying on a local text file.

### 🤖 AI Integration Features
- [ ] **Prompt Generator**: Automatically generate a text file with a "ready-to-paste" prompt for ChatGPT alongside the CSV.
      *Example: "I have these wines available... recommend 3 for a steak dinner."*
- [ ] **Taste Profile Filtering**: Pre-filter wines by "Full-bodied", "Dry", or "Fruity" if available in the metadata.
