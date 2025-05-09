import requests
import pandas as pd
import matplotlib.pyplot as plt

# Base URL for COVID19 API
API_URL = "https://api.covid19api.com/summary"

def fetch_covid_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raises error for bad responses
        data = response.json()
        return data
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return None

def display_global_summary(data):
    global_stats = data["Global"]
    print("\n🌍 Global COVID-19 Summary:")
    print(f"Total Confirmed: {global_stats['TotalConfirmed']:,}")
    print(f"Total Deaths:    {global_stats['TotalDeaths']:,}")
    print(f"Total Recovered: {global_stats['TotalRecovered']:,}")

def display_country_summary(data, country_name):
    countries = data["Countries"]
    country_data = next((c for c in countries if c["Country"].lower() == country_name.lower()), None)
    
    if not country_data:
        print(f"❌ No data found for country: {country_name}")
        return

    print(f"\n📊 COVID-19 Summary for {country_data['Country']}:")
    print(f"New Confirmed:   {country_data['NewConfirmed']:,}")
    print(f"Total Confirmed: {country_data['TotalConfirmed']:,}")
    print(f"New Deaths:      {country_data['NewDeaths']:,}")
    print(f"Total Deaths:    {country_data['TotalDeaths']:,}")
    print(f"Total Recovered: {country_data['TotalRecovered']:,}")

def plot_top_countries(data, top_n=10):
    df = pd.DataFrame(data["Countries"])
    top = df.sort_values(by="TotalConfirmed", ascending=False).head(top_n)
    plt.figure(figsize=(10,6))
    plt.bar(top['Country'], top['TotalConfirmed'], color='skyblue')
    plt.xticks(rotation=45)
    plt.title(f"Top {top_n} Countries by Confirmed COVID-19 Cases")
    plt.xlabel("Country")
    plt.ylabel("Total Confirmed Cases")
    plt.tight_layout()
    plt.show()

def main():
    print("=== COVID-19 Global Data Tracker ===")
    data = fetch_covid_data()
    
    if not data:
        return

    display_global_summary(data)
    
    while True:
        country = input("\nEnter a country name to view details (or type 'exit'): ")
        if country.lower() == 'exit':
            break
        display_country_summary(data, country)
    
    show_plot = input("\nWould you like to see a chart of the top affected countries? (y/n): ")
    if show_plot.lower() == 'y':
        plot_top_countries(data)

    print("\n✅ Program finished.")

if __name__ == "__main__":
    main()
