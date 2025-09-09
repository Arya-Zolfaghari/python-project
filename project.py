import pandas as pd

# _____________________________________________________________________________________________


def load_data(FPATH="tehran_property_prices_sept2025.csv"):

    D = pd.read_csv(FPATH)
    print("Columns in the dataset:", D.columns)

    return D


# _____________________________________________________________________________________________



def convert_to_usd(P_toman, E_rate=106650):
    return P_toman / E_rate


# _____________________________________________________________________________________________



def get_price_by_region(region, DATA):

    if 'District' in DATA.columns:
        R_data = DATA[DATA['District'] == region]

    elif 'Region' in DATA.columns:
        R_data = DATA[DATA['Region'] == region]

    else:
        raise KeyError("Neither 'District' nor 'Region' column found in the data")


    if not R_data.empty:
        return R_data['Price_Toman_per_m2'].values[0]

    else:
        raise ValueError(f"Region {region} not found in data")


# _____________________________________________________________________________________________



def calculate_average_price(D):
    return D['Price_Toman_per_m2'].mean()


# _____________________________________________________________________________________________


def main():
    data = load_data()
    print("Welcome to the Tehran Property Price CLI!")
    while True:
        print("\nOptions:")
        print("1. Get price by region")
        print("2. Calculate average price")
        print("3. Convert price to USD")
        print("4. Exit")
        choice = input("Choose an option (1/2/3/4): ")

        if choice == "1":
            region = input("Enter the region number (e.g., Region 1 or District 2): ")
            try:
                price = get_price_by_region(region, data)
                print(f"The price of {region} is {price} Toman per m².")
            except (ValueError, KeyError) as e:
                print(e)
        elif choice == "2":
            avg_price = calculate_average_price(data)
            print(f"The average price in Tehran is {avg_price:.2f} Toman per m².")
        elif choice == "3":
            region = input("Enter the region number (e.g., Region 1 or District 2): ")
            try:
                price = get_price_by_region(region, data)
                usd_price = convert_to_usd(price)
                print(f"The price of {region} in USD is {usd_price:.2f}.")
            except (ValueError, KeyError) as e:
                print(e)
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")



# _____________________________________________________________________________________________






if __name__ == "__main__":
    main()
