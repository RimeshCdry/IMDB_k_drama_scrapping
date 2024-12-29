title = movie.find("h3", class_= "ipc-title__text").text
        year = movie.find("span", class_="sc-300a8231-7 eaXxft dli-title-metadata-item").text.strip("()")
        rating = movie.find("span", class_ = "ipc-rating-star--rating").text
        print(f"{title} ({year}) - Rating: {rating}")