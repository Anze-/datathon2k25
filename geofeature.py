import re
import pandas as pd

GEOFEATURES_PATH = "./geofeature.csv"
DEMOGRAPHICS_PATH = "./us-cities-demographics.csv"
CITIES_PATH = "./geonames-all-cities-with-a-population-1000.csv"

class GeofeaturesSwagger:
    def __load_data(self):
        cdb = pd.read_csv(CITIES_PATH, sep=';', header=0)
        cof = cdb[cdb['Country Code'].isin(['US','AU'])]
        cof = cof[cof['Population']>10000]
        
        usc = pd.read_csv(DEMOGRAPHICS_PATH, sep=';', header=0)
        usc = usc[['City','State Code','Median Age','Male Population','Female Population','Foreign-born']].drop_duplicates()
        USCODES = usc['State Code'].unique()
        merged_df = pd.merge(
            cof,
            usc,
            left_on=['Name', 'Admin1 Code'],
            right_on=['City', 'State Code'],
            how='left'
        )

        geo_df = merged_df[['ASCII Name', 'Alternate Names', 'Feature Class',
               'Feature Code', 'Country Code',
               'Admin1 Code', 'Population', 'Elevation','Timezone', 'Coordinates', 'City', 'State Code',
               'Median Age', 'Male Population', 'Female Population', 'Foreign-born']]

        blacklist = ['Enterprise','Summit','Justice',"Mobile","Opportunity","Mission","Orange","March","Central"]


        for wrd in blacklist:
            geo_df = geo_df[geo_df['ASCII Name']!=wrd]

        cities = geo_df['ASCII Name'].values
        cities = [city.lower() for city in cities]
        self.cities_set = set(city.lower() for city in cities)

    def __init__(self, path):
        self.df = pd.read_csv(path, header=None)
        self.rev_index = {}
        # for each cell in col 5
        for i in range(len(self.df)):
            cell = self.df.iloc[i, 5]
            # consider cell as a list
            cell = cell.strip("[]").replace("'", "").split(" ")
            # for each element in cell
            for item in cell:
                item = item.lower()
                # if item is not in rev_index, add it
                if item not in self.rev_index:
                    self.rev_index[item] = []
                # append the index to the list
                self.rev_index[item].append(i)

        self.__load_data()

        self.regex_pattern = re.compile(
            r'\b(?:' +
            '|'.join(re.escape(city) for city in self.cities_set) +
            r')\b',
            flags=re.IGNORECASE
        )
        print(self.regex_pattern)

    def __contains_city(self, text: str):
        match = self.regex_pattern.search(text)
        if match:
            return True, match.group(0), match.start()
        return False, "", -1

    def compute_relevant_documents(self, query):
        found, city, pos = self.__contains_city(query)
        print(found,city,pos)
        city = city.lower()
        if found and city in self.rev_index:
            return self.rev_index[city]
        return [] 
