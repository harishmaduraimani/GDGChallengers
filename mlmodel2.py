import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

def ml(new_business):
# Sample dataset with equal length for both lists
    data = {
        'Business Name': ['fafefs dental care', 'dfsf tooth', 'gegr teeth', 'rthrg dentals', 'erger dental care', 'sfsfs dentals', 
                        'sfsfs dental clinic','kafef saloons', 'jazz saloons', 'fird haircuts', 'grsd haircuts', 'gdfrg saloons','dkffdg haircuts', 'derr saloon', 'grge beauty',
                        'tony and guy', 'green trends', 'root&rough', 'grewe beauty',

                        'cdot Hospital', 'RFERTE Hospital', 'sdwef Hospital', 'shiv  Hospital', 'medsi Hospital', 'kksse Hospital', 'Msk Clinic',
                        'vimal Clinic', 'jkks Clinic', 'maedx Clinic', 'Clinic',

                        'kumarn bike service', 'jk bikes', 'gkds bikes', 'tvs bikes', 'pksd bikes', 'detrtr bike service',
                            'dfsffere bikes', 'car solution', 'car service',
                        'jazz bikes and cars', 'john car service', 'halz bike and car service', 'faxes car services',

                        'snamuga stores', 'arulmurgan supermarket', 'pooja supermarket', 'fulix groceries', 'lxu groceries',
                            'jagan hypermarket', 'kays hypermarket', 'dogen supermarket',
                        'kuss stores', 'naeed fruits', 'nasfd vegtables', 'dfsdfs fruits',
                            'sdfsdfs vegtables', 'sdfsdfs fruits&vegtables', 'sdfsf fruits&vegetables',
                        'fsdfsdf stores', 'effsef instamart', 'rferfw instamart', 'lgdg shop', 'fsfs shop',

                        'Lenskart', 'sathya agencies', 'vasanthan & co', 'the lens',
                            'lens makers', 'glasses', 'tiles agency', 'tiles', 'agencies', 'sathya mobiles',
                        'the chennai mobiles', 'the cycle king', 'the motors of cycles',
                            'riderscycle', 'bicycles', 'TVS', 'bikes', 'motors bike', 'sanmugam cars', 'raga cars',

                        'Dominos Pizza', 'Pizza hub', 'kics burgar', 'burgar king', 'waffals king',
                            'the waffal', 'cafe', 'the cafe kin', 'tea time', 'karu coffee', 'king coffee', 'tea boy',
                            'juice king', 'juiccie', 'THE snacks', 'snacks king', 'vetri snacks&juice', 'madurai jigaruthanda', 
                        'maran jigaruthanda', 'famous jigaruthanda', 'anbu barkery', 'ahfvd cake', 'abi sweets', 'elite barkery',
                            'hdfs cake', 'fdsf sweets',

                        'sanmugam mobile service', 'gbs service', 'tech solution', 'tech service', 'solvo tech', 
                        'vk mobile service', 'lapo laptop service', 'id laptop service', 'makdj mobile service',

                        'amman Hotel', 'sungam Restaurant', 'mr.beast Hotel', 'navis Kitchen', 'kurans Kitchen', 'yaks Kitchen', 'uvals Resturent',
                            'akshara veg', 'talba veg',

                        'apollo pharmarcy', 'anbu pharmarcy', 'mantra medicals', 'siva medicals', 'medplus pharmarcy', 'sakti pharmarcy',
                        
                        'soft courier','hard courier','sdww courier','st courier','sdwef package','sdfcs package service','dfsfs parcel service',
                        'dsfwe parcels',
                        
                        'sdadsd studio','dfwsfsf prints','dfvsdfs studio and prints','erwerf studio & prints','dfsdfsf print shops',
                        'sdfdf xerox','sdfsf xerox dsf','sdff xerox shop','dfd studio','dfrfde photos','fese photos','fsfs photo&VIDEO',
                        'FSFSFES photo&video',
                        
                        'gvuygu tution center','hbjhbjb tution center','hbhguih tution center','ygugvuy tution','uyuhv tution','yvuv study',
                        'gvuvuv study','hgvjvuv books',
                        'stationary','gvuyvuv books','hbhjhbujy stationaries','sdsdsz stationaries','sdsds stationary','dfdfd study','dfswff book',
                        'fefsf book','bdfcdfd book center',
                        
                        'fssf Electronics','asdadsd Electronics service','sdasdas Electronics service','gthrfhbr Electronics','rgegerge Electronics',
                        'trer Electronic shop',
                        'fffeft55 Electronic shop',
                            'fstyhhy556sf Electronics','fsdfedfsf Electronics'],
        
        'Category': ['Dental', 'Dental', 'Dental', 'Dental', 'Dental', 'Dental', 'Dental',
                    
                    'Saloons', 'Saloons', 'Saloons', 'Saloons', 'Saloons', 'Saloons', 'Saloons', 'Saloons', 'Saloons', 'Saloons', 'Saloons',
                    'Saloons',
                    
                    'Hospital', 'Hospital', 'Hospital', 'Hospital', 'Hospital', 'Hospital', 'Hospital', 'Hospital', 'Hospital', 'Hospital',
                    'Hospital',

                    'Vehicles Services', 'Vehicles Services', 'Vehicles Services', 'Vehicles Services', 'Vehicles Services', 'Vehicles Services',
                    'Vehicles Services', 'Vehicles Services', 'Vehicles Services', 'Vehicles Services', 'Vehicles Services', 'Vehicles Services',
                    'Vehicles Services',

                    'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable', 
                    'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable',
                    'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable',
                    'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable',
                    'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable',
                    'Groceries,Fruits or Vegetable', 'Groceries,Fruits or Vegetable',

                    'Retail', 'Retail', 'Retail', 'Retail', 'Retail', 'Retail', 'Retail', 'Retail', 'Retail', 'Retail',
                    'Retail', 'Retail', 'Retail', 'Retail', 'Retail', 'Retail', 'Retail', 'Retail', 'Retail',

                    'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food',
                    'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food',
                    'Food', 'Food', 'Food','Food','Food','Food',

                    'Laptop or Mobile Service', 'Laptop or Mobile Service', 'Laptop or Mobile Service', 'Laptop or Mobile Service',
                    'Laptop or Mobile Service', 'Laptop or Mobile Service', 'Laptop or Mobile Service', 'Laptop or Mobile Service',
                        'Laptop or Mobile Service',

                    'Restaurant', 'Restaurant', 'Restaurant', 'Restaurant', 'Restaurant', 'Restaurant', 'Restaurant', 'Restaurant', 'Restaurant',

                    'Pharmacy', 'Pharmacy', 'Pharmacy', 'Pharmacy', 'Pharmacy', 'Pharmacy',
                    
                    'Courier','Courier','Courier','Courier','Courier','Courier','Courier','Courier',

                    'Studio&Print shop','Studio&Print shop','Studio&Print shop','Studio&Print shop','Studio&Print shop','Studio&Print shop',
                    'Studio&Print shop',
                    'Studio&Print shop','Studio&Print shop','Studio&Print shop','Studio&Print shop','Studio&Print shop','Studio&Print shop',
                    
                    'Education','Education','Education','Education','Education','Education','Education','Education','Education','Education',
                    'Education','Education','Education','Education','Education','Education','Education',
                    'Electronic','Electronic','Electronic','Electronic','Electronic','Electronic','Electronic','Electronic','Electronic']


    }

    df = pd.DataFrame(data)

    # Feature extraction using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['Business Name'])  # Convert business names to features
    y = df['Category']  # Labels

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train a Naive Bayes classifier
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Display results


    # Testing with new input
    new_business_tfidf = vectorizer.transform(new_business)  # Convert the new input to the same TF-IDF format
    predicted_category = model.predict(new_business_tfidf)

    return predicted_category[0]


