
import pandas as pd
import plotly.express as px

class plots:
    def __init__(self) -> None:
        self.df = pd.read_csv('../data/processed/df_duration_prepared.csv',index_col=0)
        self.df['publish_time'] = self.df.publish_time.astype('datetime64[ns]')
        self.df['trending_date'] = self.df.trending_date.astype('datetime64[ns]')


    def get_category_names(self):
        return list(self.df.category_title.unique())

    def category_views(self,categories):
        df = self.df[self.df.category_title.isin(categories)]
        cat = df.category_title.unique()
        cat_views = df.groupby('category_title')['views'].mean()[cat].values
        cat_count =df.category_title.value_counts()[cat]
        fig = px.scatter(df,'trending_date','views',log_y=True,size='duration_in_minutes',
                         size_max=30,color = 'category_title',facet_col='category_title',labels = {"trending_date":''},
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

        fig.update_traces(textposition='top center')

        fig.update_layout(
            title_text='',showlegend = False,width=1500, height=500
        )
        fig.update_layout({
            'plot_bgcolor':'rgba(0, 0, 0, 0)',
            'paper_bgcolor':'rgba(0, 0, 0, 0)',
        })

        fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', size=14))

        return fig