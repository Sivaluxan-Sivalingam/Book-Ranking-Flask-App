import requests
import mysql.connector
import json
import schedule
import time 
from datetime import datetime, timedelta
import pytz

def extract_and_store_data():
    # Define the API endpoint URL
    url = "https://api.nytimes.com/svc/books/v3/lists/full-overview.json?api-key=k1vdZZ7QRLbV8dFSEsw2iMk4qbch0pAS"

    # Make a GET request to the API
    response = requests.get(url)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="dataprogramming-project.c1ge4vi7lkbt.us-east-2.rds.amazonaws.com",
        user="admin",
        password="Sivaluxan",
        database="BOOK_RANK_DB"
    )

    #define book_id variable
    book_id=1
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()
        
        # Process the data as needed
        # print(data)
        # print(data["results"])
        # print(type(data["results"]))
        # print(data["results"]["lists"])
        # print(len(data["results"]["lists"]))
        # print(data["results"]["lists"][0]["list_id"])

        lists=data["results"]["lists"]
        cursor = conn.cursor()
        #store list values to list table
        for list_data in lists:
            list_id=list_data["list_id"]
            list_name=list_data["list_name"]
            list_name_encoded=list_data["list_name_encoded"]
            display_name=list_data["display_name"]
            updated=list_data["updated"]
            list_image=list_data["list_image"]
            list_image_width=list_data["list_image_width"]
            list_image_height=list_data["list_image_height"]
            #display
            print(list_id)
            # Define and execute SQL insert query
            sql_query = "INSERT INTO list_table(list_id, list_name, list_name_encoded, display_name, updated, list_image, list_image_width, list_image_height) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_query,(list_id, list_name, list_name_encoded, display_name, updated, list_image, list_image_width, list_image_height))
            
            books=list_data["books"]
            # print(books)
            
            for book in books:
                age_group=book["age_group"]
                amazon_product_url=book["amazon_product_url"]
                article_chapter_link=book["article_chapter_link"]
                author=book["author"]
                book_image=book["book_image"]
                book_uri=book["book_uri"]
                btrn=book["btrn"]
                contributor=book["contributor"]
                contributor_note=book["contributor_note"]
                created_date=book["created_date"]
                description=book["description"]
                first_chapter_link=book["first_chapter_link"]
                price=book["price"]
                publisher=book["publisher"]
                book_rank=book["rank"]
                rank_last_week=book["rank_last_week"]
                sunday_review_link=book["sunday_review_link"]
                title=book["title"]
                weeks_on_list=book["weeks_on_list"]
                
                #insert book data to books_table
                sql_query_book = "INSERT INTO book_table(book_id ,list_id , age_group , amazon_product_url, article_chapter_link,author ,book_image , book_uri , btrn, contributor, contributor_note, created_date , description, first_chapter_link ,price , publisher ,book_rank , rank_last_week , sunday_review_link , title, weeks_on_list ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_query_book,(book_id ,list_id , age_group , amazon_product_url, article_chapter_link,author ,book_image , book_uri , btrn, contributor, contributor_note, created_date , description, first_chapter_link ,price , publisher ,book_rank , rank_last_week , sunday_review_link , title,weeks_on_list ))
                buy_links=book["buy_links"]
                for buy_link in buy_links:
                    print(buy_link["name"])
                    buy_link_name=buy_link["name"]
                    buy_link_url=buy_link["url"]


                    #insert book buy links data to buy_links_table
                    sql_query_buy_links = "INSERT INTO buy_links_table(book_id ,list_id , name, url) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql_query_buy_links,(book_id ,list_id , buy_link_name , buy_link_url))
                book_id+=1

        # Commit the transaction
        conn.commit()
            
        # Close cursor and connection
        cursor.close()
        conn.close()
    else:
        print("Failed to retrieve data from the API. Status code:", response.status_code)



# Get the timezone for Eastern Time (ET)
eastern = pytz.timezone('America/Toronto')

# Calculate the target run time for today at 12:30 PM ET
target_time = datetime.now(eastern).replace(hour=12, minute=30, second=0, microsecond=0)

# Schedule the extract_and_store_data function to run today at 12:30 PM ET
schedule.every().day.at(target_time.strftime("%H:%M")).do(extract_and_store_data)

# Infinite loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)