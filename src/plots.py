
import pandas as pd
import plotly.express as px

class plots:
    def __init__(self) -> None:
        self.df = pd.read_csv('../data/processed/df_duration_prepared.csv',index_col=0)
        self.df['publish_time'] = self.df.publish_time.astype('datetime64[ns]')
        self.df['trending_date'] = self.df.trending_date.astype('datetime64[ns]')


    def get_category_names(self):
        return list(self.df.category_title.unique())
    
    def get_country_name(self):
        return list(self.df.Country.unique())


    def category_views(self,categories,countries):
        df = self.df[(self.df.category_title.isin(categories)) &(self.df.Country.isin(countries))]
        # cat_count = int(df.category_title.value_counts().sum())
        # print(cat_count)
        cat = df.category_title.unique()
        cat_views = df.groupby('category_title')['views'].mean()[cat].values
        cat_count =df.category_title.value_counts()[cat]
        fig = px.scatter(df,'trending_date','views',log_y=True,size='duration_in_minutes',
                         size_max= 50,color = 'category_title',facet_col='category_title',labels = {"trending_date":''},
                        facet_col_spacing=.007,color_discrete_sequence=px.colors.qualitative.Dark24)
        for i in range (len(cat_views)):
        #     print(cat_views[i])
            fig.add_hline(cat_views[i],col=i+1,line_dash = 'dot')
            fig.add_annotation(xref='x domain',
                               yref='y domain',
                               x=0.50,
                               y=0.99,
                               text = str(cat_count[i]),
                               row = 1,col=i+1,showarrow = False,
                               font=dict(
                                            family="sans serif",
                                            size=18,
                                            color=px.colors.qualitative.Dark24[i]
            ))

        fig.for_each_annotation(lambda a: a.update(text= a.text.split("=")[-1].split('&')[-1] ,
        font=dict(
                                            family="sans serif",
                                            size=14,
                                            # color=px.colors.qualitative.Dark24[i]
            )))

        # fig.update_traces(textposition='top center')

        fig.update_layout(
            title_text='Categories Views & The Length Of Each Video',title_x=0.5,showlegend = False
        )
        fig.update_layout({
            'plot_bgcolor':'rgba(0, 0, 0, 0)',
            'paper_bgcolor':'rgba(0, 0, 0, 0)',
        })

        fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', size=14))

        return fig


    def days_views(self,categories,countries):
        # print(countries)
        df = self.df[(self.df.category_title.isin(categories)) &(self.df.Country.isin(countries))]

        days = df.puplished_day.value_counts().sort_values()
        puplished_day_views_norm = df.groupby('puplished_day')['views'].sum()[days.index] / days

        # print(days, puplished_day_views_norm)

        fig = px.bar(df,y = days.index,x = days,color_continuous_scale='algae',
                orientation='h',color = puplished_day_views_norm,labels= {'x': 'NO. Uploaded Videos','y':'','color':'views'})

        fig.update_layout(
            title_text='Most viewed days & Summtion of Views of each day',title_x=0.5
        )
        fig.update_layout({
            'plot_bgcolor':'rgba(0, 0, 0, 0)',
            'paper_bgcolor':'rgba(0, 0, 0, 0)',
        })

        return fig


    def views_country(self,countries):
        df = self.df[self.df.Country.isin(countries)]
        views_date = df.groupby(['category_title','trending_date','Country'])['views'].mean()
        views_date = views_date.reset_index(level=[0,2])
        if len(countries) == len(list(self.df.Country.unique())):
            fig = px.line(views_date,x = views_date.index ,y = views_date.views,
                log_y = True,animation_frame='category_title')
        else : 
            fig = px.line(views_date,x = views_date.index ,y = views_date.views,
                log_y=True, color = 'Country',animation_frame='category_title')
        
        fig.update_layout(
        title_text='Countries Views on each Category' ,title_x=0.5
        )
        fig.update_layout({
            'plot_bgcolor':'rgba(0, 0, 0, 0)',
            'paper_bgcolor':'rgba(0, 0, 0, 0)',
        })
        return fig


    def Views_vs_VideoLength(self,categories,countries):
        df = self.df[(self.df.category_title.isin(categories)) &(self.df.Country.isin(countries))]
        fig = px.scatter(df,'duration_in_minutes','views')

        fig.update_layout(
        title_text='Views_vs_VideoLength' ,title_x=0.5
        )
        fig.update_layout({
            'plot_bgcolor':'rgba(0, 0, 0, 0)',
            'paper_bgcolor':'rgba(0, 0, 0, 0)',
        })
        return fig




