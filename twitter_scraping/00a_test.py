
import pandas as pd
search_term = 'the_first_temptation_of_christ'
import_path = '.\\data\\' + search_term + '.xlsx'

data = pd.read_excel(import_path, index_col=0)

print(data['id'])
