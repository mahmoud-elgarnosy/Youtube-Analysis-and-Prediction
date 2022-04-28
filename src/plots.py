
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go


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
                                            size=abs(- (len(df.category_title.unique())/-.99) - 9) * 2.5,
                                            # color=px.colors.qualitative.Dark24[i]
            )))

        # fig.update_traces(textposition='top center')

        fig.update_layout(
            title_text='Categories Views & The Length Of Each Video',title_x=0.5,showlegend = False,
             yaxis = dict(
                        tickfont = {'size' : 15},
                        title_font_size = 20),
            xaxis = dict(
                        tickfont = {'size' : 15},
                        title_font_size = 20),
             title_font_size = 25)
        
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
            title_text='Most viewed days & Summtion of Views of each day',title_x=0.5,
             yaxis = dict(
                        tickfont = {'size' : 15},
                        title_font_size = 20),
            xaxis = dict(
                        tickfont = {'size' : 15},
                        title_font_size = 20),
             title_font_size = 25)
        fig.update_layout({
            'plot_bgcolor':'rgba(0, 0, 0, 0)',
            'paper_bgcolor':'rgba(0, 0, 0, 0)',
        })

        fig.update_layout(legend = dict(font = dict(family = "Courier", size = 15, color = "black")),
                  legend_title = dict(font = dict(family = "Courier", size = 20, color = "blue")))

        return fig


    def views_country(self,countries):
        df = self.df[self.df.Country.isin(countries)]
        views_date = df.groupby(['category_title','trending_date','Country'])['views'].mean()
        views_date = views_date.reset_index(level=[0,2])
        if len(countries) >= 3:
            fig = px.line(views_date,x = views_date.index ,y = views_date.views,
                log_y = True,animation_frame='category_title')
        else : 
            fig = px.line(views_date,x = views_date.index ,y = views_date.views,
                log_y=True, color = 'Country',animation_frame='category_title')
        
        fig.update_layout(
        title_text='Countries Views on each Category' ,title_x=0.5,
          yaxis = dict(
                        tickfont = {'size' : 15},
                        title_font_size = 20),
        xaxis = dict(
                        tickfont = {'size' : 15},
                        title_font_size = 20),
        title_font_size = 25)
        fig.update_layout({
            'plot_bgcolor':'rgba(0, 0, 0, 0)',
            'paper_bgcolor':'rgba(0, 0, 0, 0)',
        })

        fig.update_layout(legend = dict(font = dict(family = "Courier", size = 20, color = "black")),
                  legend_title = dict(font = dict(family = "Courier", size = 25, color = "blue")))
                
        return fig


    def Views_vs_VideoLength(self,categories,countries):
        df = self.df[(self.df.category_title.isin(categories)) &(self.df.Country.isin(countries))]
        duration_labels = ['<5', '5-15', '15-25', '25-35','>35']
        cut_bins = [0, 5, 15, 25, 35,np.max(df.duration_in_minutes)]
        df['duration_bins'] = pd.cut(df.duration_in_minutes, bins=cut_bins, labels=duration_labels)



        views_average = df.groupby('duration_bins')['views'].mean()
        fig = px.bar(x = duration_labels, y = views_average, labels = {'x': 'Duration (Minutes)', 'y': 'Average of views'},
      text_auto = '0.2s')

        fig.update_layout(title_text = 'Views vs Videos Duration', title_x = .5,
            yaxis = dict(
                        tickfont = {'size' : 15},
                        title_font_size = 20),
            xaxis = dict(
                        tickfont = {'size' : 15},
                        title_font_size = 20),
            title_font_size = 25)
        fig.update_traces(textfont_size = 20)
        # views_average
        fig.update_layout({
            'plot_bgcolor':'rgba(0, 0, 0, 0)',
            'paper_bgcolor':'rgba(0, 0, 0, 0)',
        })

        return fig


    def most_trending_videos(self,categories,countries):
        df2 = pd.read_csv('../data/external/final_data/final_data.csv',index_col=0)
        df2.drop(df2[df2.video_id == '#NAME?'].index,inplace=True)
        df = df2[(df2.category_title.isin(categories)) &(df2.Country.isin(countries))]
        most_trending_videos_id = list(df.video_id.value_counts()[:5].index)
        most_trending_videos_count = list(df.video_id.value_counts()[:5].values)
        most_trending_videos_data = df[df.video_id.isin(most_trending_videos_id)]
        most_trending_videos_data.drop_duplicates(subset = 'video_id', keep = 'last', inplace = True )
        most_trending_videos_data = most_trending_videos_data.iloc[pd.Series(pd.Categorical(most_trending_videos_data.video_id, 
                                        categories=most_trending_videos_id, 
                                        ordered=True))\
                .sort_values()\
                .index\
            ]
        categories = most_trending_videos_data.category_title.values
        countries = most_trending_videos_data.Country.values
        views = most_trending_videos_data.views.values
        layout = go.Layout(
                    title="Most Trending 5 Videos",
                    annotations=[
                        dict(
                            y=xpos,
                            x= float('8.5M'.strip('M')),
                            xref='x',
                            yref='y',
                            text=str(count),
                            showarrow=False,
                            font = {'size' : 20}
                        ) for xpos,ypos ,count in zip(np.arange(1,6),views, countries+ "__" + categories)
                    ],
                    yaxis=dict(
                        title="Trending Days"),
                    xaxis=dict(
                        title=" "),
                    barmode='group',
                    plot_bgcolor='rgb(233,233,233)')
        fig = go.Figure(data=[
            go.Bar(name='Views', y=np.arange(1,6), x=most_trending_videos_data.views.values,orientation='h'),
            
            go.Bar(name='Likes', y=np.arange(1,6), x=most_trending_videos_data.likes.values,orientation='h'
                ,marker = {
                'color' : 'rgba(0,128,0,1)'}),
            go.Bar(name='Dislikes', y=np.arange(1,6), x=most_trending_videos_data.dislikes.values,orientation='h',marker = {
                'color' : 'rgba(255,0,0,1)'
            }),],
                    
                        layout=layout)
        fig.update_layout(barmode='group',title_x = .5)
        fig.update_xaxes(type="log")
        fig.update_layout(yaxis = dict(
                tickmode = 'array',
                tickvals = [1, 2, 3, 4, 5],
                ticktext = most_trending_videos_count,
                tickfont = {'size' : 15},
                title_font_size = 20
            ),title_font_size = 25
            ,xaxis = dict(tickfont = {'size' : 15},title_font_size = 20 ))

        fig.update_layout(legend = dict(font = dict(family = "Courier", size = 15, color = "black")),
                  legend_title = dict(font = dict(family = "Courier", size = 30, color = "blue")))

        fig.update_layout({
            'plot_bgcolor':'rgba(0, 0, 0, 0)',
            'paper_bgcolor':'rgba(0, 0, 0, 0)',
        })

        fig.update_traces(textfont_size = 20)
        
        return fig



