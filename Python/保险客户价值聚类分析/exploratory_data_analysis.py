# 导入包
import pandas as pd
import plotly.graph_objs as go

#* 定义类
class EDAnalysis:
    def __init__(self,
                data:pd.DataFrame =None,                                                        # type: ignore
                id_col: str=None,                                                               # type: ignore
                target: str = None,                                                             # type: ignore
                cate_list: list = None,                                                         # type: ignore
                num_list: list = None,                                                          # type: ignore
            ):
        self.data = data
        self.id_col = id_col
        self.target = target
        self.num_list = num_list
        self.cate_list = cate_list

    def draw_bar(self, col_name: str):
        bar_num = self.data[col_name].value_counts()
        #! 条形图
        trace0 = go.Bar(x=bar_num.index.tolist(),
                        y=bar_num.values.tolist(),                                                          # type: ignore
                        text=bar_num.values.tolist(),                                                       # type: ignore
                        textposition='auto',
                        marker=dict(color=["blue", "red", "green", "indianred", "darkgrey"], opacity=0.5)
                        )
        data = [trace0]
        layout = go.Layout(title=f'Distribution_num of {col_name}', bargap=0.4, height=600,
                        xaxis={'title': col_name})
        fig = go.Figure(data=data, layout=layout)

        return fig

    def draw_pie(self, col_name: str):
        pie_num = self.data[col_name].value_counts()
        #! 饼图
        trace1 = go.Pie(labels=pie_num.index.tolist(),
                        values=pie_num.values.tolist(),                                                  # type: ignore
                        hole=.5,
                        marker=dict(line=dict(color='white', width=1.3))
                        )
        data = [trace1]
        layout = go.Layout(title=f'Distribution_ratio of {col_name}', height=600)
        fig = go.Figure(data=data, layout=layout)

        return fig

    def draw_bar_stack_cat(self, col_name: str):
        #! 交叉表
        cross_table = round(pd.crosstab(self.data[col_name], self.data[self.target], normalize='index') * 100, 2)
        #! 索引
        index_cols = cross_table.columns.tolist()                                                                            # type: ignore
        #! 轨迹列表
        data = []
        for i in index_cols:
            trace = go.Bar(x=cross_table[i].values.tolist(),                                                                # type: ignore
                        y=cross_table.index.tolist(),                                                                       # type: ignore
                        name=str(i),
                        orientation='h',
                        marker={'opacity': 0.8}
                    )
            data.append(trace)
            #! 布局
        layout = go.Layout(title=f'Relationship Between {cross_table.index.name} and {cross_table.columns.name}',       # type: ignore
                        bargap=0.4,
                        barmode='stack',
                        height=600,
                        xaxis={'title': '百分比'},
                        yaxis={'title': col_name}
                    )
        #! 画布
        fig = go.Figure(data=data, layout=layout)
        return fig

    def draw_histogram(self, col_name: str):
        trace = go.Histogram(x=self.data[col_name], histnorm='probability', opacity=0.8)

        data = [trace]
        layout = go.Layout(title=f'Histogram of {col_name}', height=600,
                        xaxis={'title': col_name})

        fig = go.Figure(data=data, layout=layout)
        return fig

    def draw_bar_stack_num(self, col_name: str, bins_num:int = 25):
        #! 交叉表
        x_data = pd.cut(self.data[col_name], bins=bins_num)
        cross_table = round(pd.crosstab(x_data, self.data[self.target], normalize='index') * 100, 2)
        #! 索引
        index_cols = cross_table.columns.tolist()                                                                   #type:ignore
        #! 轨迹列表
        data = []
        for i in index_cols:
            trace = go.Bar(x=cross_table.index.astype('str').tolist(),                                                  #type:ignore
                        y=cross_table[i].values.tolist(),                                                               #type:ignore
                        name=str(i),
                        orientation='v',
                        marker={'opacity': 0.8},
                    )
            data.append(trace)
            #! 布局
        layout = go.Layout(title=f'Relationship Between {cross_table.index.name} and {cross_table.columns.name}',               #type:ignore
                        bargap=0,
                        barmode='stack',
                        height=600,
                        xaxis={'title': col_name},
                        yaxis={'title': '百分比'}
                    )
        #! 画布
        fig = go.Figure(data=data, layout=layout)
        return fig

    def draw_scatter_matrix(self):
        #! 目标
        index_vals = self.data[self.target].astype('category').cat.codes

        dimension_list = []

        for i in self.num_list:
            dimension_list.append(dict(label=i, values=self.data[i]))

        trace = go.Splom(dimensions=dimension_list,
                        text=self.data[self.target],
                        marker=dict(color=index_vals,
                                    showscale=False,
                                    line_color='white', line_width=0.5)
                    )
        data = [trace]
        layout = go.Layout(title='ScatterPlot Matrix Between numeric Attributes', height=600)
        fig = go.Figure(data=data, layout=layout)

        return fig

