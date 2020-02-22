import pandas as pd

class Rating:
    
    def rate(self):
        tags = pd.read_excel('tags.xlsx')
        df1 = pd.read_excel('res.xlsx')
        df2 = pd.read_excel('results.xlsx')
        dfs = [df1, df2]
        df = pd.concat(dfs, sort=True)
        
        df['points'] = 0
        df['found_tags'] = ''
        for tag, n_points in zip(tags['tag'], tags['points']):
            mask1 = df['description'].str.contains(tag, regex = True)
            mask2 = df['tags'].str.contains(tag)
            mask3 = df['title'].str.contains(tag)
            mask4 = df['city'].str.contains(tag)
            df.loc[mask1 | mask2 | mask3 | mask4, 'points'] += n_points
            df.loc[mask1 | mask2 | mask3, 'found_tags'] += tag
           
        
        df.sort_values(by=['points'], ascending = False, inplace=True)
        df.to_excel('result.xlsx', index = False)

rating = Rating()
rating.rate()