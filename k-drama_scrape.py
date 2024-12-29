import requests
from bs4 import BeautifulSoup
import sqlite3


def options():
    print("""
        1. create_table
        2. insert_data
        3. delete_data
        4. delete_table
        """)

def create_connection():
    try:
        con = sqlite3.connect("k-drama.sqlite3")
        return con
    except Exception as e:
        print(e)
con = create_connection()
       
def create_table(con):
    try:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS dramas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                year VARCHAR(255),
                rating VARCHAR(255),
                vote_count VARCHAR(255)
            );
        """)
        
        print("Table dramas created successfully.")
        con.commit()
    except Exception as e:
        print(e)

def insert_data(con, title, year, rating, vote_count):
    
    try:
        cur = con.cursor()
        
        cur.execute(f"""
            INSERT INTO dramas (title, year, rating, vote_count)
            VALUES (?, ?, ?, ?)""", (title, year, rating, vote_count)
        )
        con.commit()
        
    except Exception as e:
        print(e)


      
def delete_data(con):
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM dramas")
        con.commit()
        
    except Exception as e:
        print(e)


def delete_table(con):
    try:
        cur = con.cursor()
        cur.execute("DROP TABLE dramas")
        print("Table dramas deleted successfully.")
        con.commit()
        
    except Exception as e:
        print(e)

base_url = "https://www.imdb.com/search/title/?title_type=tv_series&countries=KR"


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def scrape_data():
    final_page = int(input("Enter the number of pages you want to scrape (e.g., 1, 2, 3): "))
    page_no = 1
    
    while page_no <= final_page:
        # Fetch the current page
        print(f"Scraping page {page_no}...")
        response = requests.get(f"{base_url}&start={(page_no - 1) * 50 + 1}", headers=headers)
        
        if response.status_code != 200:
            print("Failed to retrieve IMDb data.")
            break
        
        soup = BeautifulSoup(response.content, "html.parser")
        movies = soup.find_all("div", class_="sc-300a8231-0 gTnHyA")

        # Stop if no more movies are found
        if not movies:
            print("No more results found.")
            break

        for movie in movies:
            title = movie.find("h3", class_= "ipc-title__text").text
            year = movie.find("span", class_="sc-300a8231-7 eaXxft dli-title-metadata-item").text.strip("()")
            rating_tag = movie.find("span", class_ = "ipc-rating-star--rating").text
            rating = rating_tag if rating_tag else "N/A"
            vote = movie.find("span", class_= "ipc-rating-star--voteCount").text
        
            vote_count = vote.strip().strip('()').replace('&nbsp;', '').strip() if vote else "N/A"  
            # print(f"{title} ({year}) - Rating: {rating} ({vote_count} votes)")
            
            insert_data(con,title[3:].strip(), year, rating, vote_count)
            
        page_no += 1  # Move to the next page
        print(f"\nSuccessfully Data Scrapped from page: {page_no - 1}\n")

 
def main():
    if __name__ == "__main__":
        options()
        
        choice = input("Enter your choice: ")
        if choice == "1":
            create_table(con)
        elif choice == "2":
            scrape_data()
        elif choice == "3":
            delete_data(con)
            print("Data deleted successfully.")
        elif choice == "4":
            delete_table(con)
        else:
            print("Invalid choice.")
            
main()
