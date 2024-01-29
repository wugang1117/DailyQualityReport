from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash
import pandas as pd
import dash_bootstrap_components as dbc
from SqlHelper import MysqlHelp
from selenium import webdriver
import pymssql

# Initialize the app
dash.register_page(__name__)

pagesize = 10

layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Div(
                            [
                                html.H1('Daily Quality Report'),
                            ]), style={'padding': '10px', 'background-color': '#00CCFF', 'text-align': 'center', }),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(id='time-graph_dqr'), width=4, ),
                        # dbc.Col(dcc.Graph(id='qty-graph_hs'), width=3),
                        dbc.Col(html.Div(
                            [
                                html.H3('Quality Inspection Data', style={'font-weight': 'normal'}),
                                dash_table.DataTable
                                    (
                                    id='quality-graph_dqr', page_size=pagesize,
                                    style_header={
                                        'background-color': '#e3f2fd',
                                        'border': '1px solid',
                                        'font-family': 'Times New Romer',
                                        'font-weight': 'bold',
                                        'text-align': 'center',
                                        'font-size': "20px",
                                    },
                                    style_data={
                                        'background-color': '#e3f2fd',
                                        'border': '1px solid',
                                        'text-align': 'left',
                                        'font-size': "20px",
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {'row_index': 'odd'},
                                            'backgroundColor': 'rgb(220, 220, 220)',
                                        },
                                        # {
                                        # 'if': {'row_index': 'even'},
                                        # 'backgroundColor': '#66FFFF',
                                        # },
                                        {
                                            'if': {'column_id': 'WO'},
                                            'textAlign': 'right'
                                        },
                                        {
                                            'if': {'column_id': 'CODE'},
                                            'textAlign': 'right'
                                        },
                                        {
                                            'if': {'column_id': 'REASON'},
                                            'textAlign': 'right'
                                        },
                                        {
                                            'if': {'column_id': 'NG_QTY'},
                                            'textAlign': 'right'
                                        },
                                        {
                                            'if': {'column_id': 'POSITION'},
                                            'textAlign': 'right'
                                        },
                                    ],
                                ),
                            ]), width=6, style={'margin-top': '30px'}),
                    ],
                ),

                dbc.Row(
                    [
                        #rework graph
                        dbc.Col(
                            dcc.Graph(id='rework-graph_dqr'), width=4, ),
                        # dbc.Col(dcc.Graph(id='qty-graph_hs'), width=3),
                        #rework table
                        dbc.Col(html.Div(
                            [
                                html.H3('Rework Data', style={'font-weight': 'normal'}),
                                dash_table.DataTable
                                    (
                                    id='rework-table_dqr', page_size=pagesize,
                                    style_header={
                                        'background-color': '#e3f2fd',
                                        'border': '1px solid',
                                        'font-family': 'Times New Romer',
                                        'font-weight': 'bold',
                                        'text-align': 'center',
                                        'font-size': "20px",
                                    },
                                    style_data={
                                        'background-color': '#e3f2fd',
                                        'border': '1px solid',
                                        'text-align': 'left',
                                        'font-size': "20px",
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {'row_index': 'odd'},
                                            'backgroundColor': 'rgb(220, 220, 220)',
                                        },
                                        # {
                                        # 'if': {'row_index': 'even'},
                                        # 'backgroundColor': '#66FFFF',
                                        # },
                                        {
                                            'if': {'column_id': 'Reason'},
                                            'textAlign': 'right'
                                        },
                                        {
                                            'if': {'column_id': 'WO'},
                                            'textAlign': 'right'
                                        },
                                        {
                                            'if': {'column_id': 'Itemcode'},
                                            'textAlign': 'right'
                                        },
                                        {
                                            'if': {'column_id': 'Process'},
                                            'textAlign': 'right'
                                        },

                                    ],
                                ),
                            ]), width=6, style={'margin-top': '30px'}),
                    ],
                ),
            ],
            fluid=True,
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Interval(id="interval-all_dqr", interval=1000 * 1000, n_intervals=0)),
            ],
        ),

    ]
)

@callback(
    Output("time-graph_dqr", 'figure'),
    Output("quality-graph_dqr", 'data'),
    Output("rework-graph_dqr", 'figure'),
    Output("rework-table_dqr", 'data'),
    Input("interval-all_dqr", "n_intervals")
)


def set_table_data(inter):
    global data

    querystr = " EXEC prod.dbo.SP_GetDailyQualityReport"
    qualitydata = MysqlHelp().select_exec_sp(querystr)
    #print(qualitydata)
    #print(len(qualitydata))

    random_x = []
    random_y = []
    random_z = []
    ng_num = 0
    for i in range(len(qualitydata)):
        if i == 0:#第一个reason
            lastReason = qualitydata[i][2]
            random_x.append(qualitydata[i][2])
            ng_num = ng_num + qualitydata[i][3]
            if i == len(qualitydata) - 1:  # 所有循环结束，最后两个reason相同，保存最后一个reason对应的纵坐标
                random_y.append(ng_num)
        else:#第二个以后的reason
            if lastReason==qualitydata[i][2]:#当前reason和上一个reason是同一个reason
                ng_num = ng_num+qualitydata[i][3]#累加不合格数目
                if i == len(qualitydata)-1:#所有循环结束，最后两个reason相同，保存最后一个reason对应的纵坐标
                    random_y.append(ng_num)
            else:                                #当前reason和上一个reason不是同一个reason
                random_x.append(qualitydata[i][2])#保存新的reason
                random_y.append(ng_num)           #保存上一个reason对应的纵坐标，然后初始化成新的reason的ng_num，重新开始累加不合格个数
                ng_num=qualitydata[i][3]          #初始化成新的reason的ng_num
                lastReason = qualitydata[i][2]        #保存最新的reason
                if i == len(qualitydata)-1:#所有循环结束，最后两个reason相同，保存最后一个reason对应的纵坐标
                    random_y.append(ng_num)


        #print(random_x,i)

    figure_quality = {

        'data': [

            {'x': random_x, 'y': random_y, 'type': 'bar', 'name': "Unqualified point"},
            {'x': 0, 'y': 0, 'type': 'bar', 'name': "Pro.Qty"}
        ],

        'layout': {
            'title': 'Quality Status Chart'
        }

    }

    # 质检数据
    qlabels = ['WO', 'CODE', 'REASON', 'NG_QTY', 'POSITION']
    qualitydata = []

    querystr = " EXEC prod.dbo.SP_GetDailyQualityReport"
    qualitydata = MysqlHelp().select_exec_sp(querystr)
    qdata = pd.DataFrame.from_records(qualitydata, columns=qlabels)

    #sql = " select rsl.DEFECT_REASON,rsl.WO,rsl.FG_CODE,rsl.PROCESS_CODE,rsl.COMPONENT_LOCATION,sum(rsl.QTY) [Qty] from BARCODESERVER.prod.dbo.RWC_STATION_LOGSHEET rsl where  1=1 and ORGANIZATION_ID='102'   and Type='Rework' and CONVERT(varchar(10), RECEIVE_DATE,120)=CONVERT(varchar(10), GETDATE()-1,120) and rsl.REPAIR_DATE is not Null group by rsl.DEFECT_REASON,rsl.WO,rsl.FG_CODE,rsl.PROCESS_CODE ,rsl.COMPONENT_LOCATION "
    sql = " EXEC prod.dbo.SP_GetDailyQualityReport_rework"
    reworkdata = MysqlHelp().select_exec_sp(sql)
    #print(sql)
    #print("################")
    #print(len(reworkdata))
    #print(reworkdata)
    #reworklabel = ['TYPE', 'RECEIVE_DATE', 'REPAIR_DATE', 'WO', 'COMPONENT_LOCATION','ITEM_CODE','QTY','CREATION_DATE']
    reworklabel = ['Reason','WO', 'Itemcode', 'Process', 'location', 'Qty']


    i =0
    random_x = []
    random_y = []
    random_z = []
    ng_num = 0
    for i in range(len(reworkdata)):
        if i == 0:#第一个reason
            #print("@@@@@@@@@1")
            #print(i)
            #print("reworkTableData[i][0]:\n",reworkdata)
            if reworkdata[i][1]==None:
                lastReason = 'None'
            else:
                lastReason = reworkdata[i][0]
            random_x.append(reworkdata[i][0])
            ng_num = ng_num + reworkdata[i][5]
            if i == len(reworkdata) - 1:  # 所有循环结束，最后两个reason相同，保存最后一个reason对应的纵坐标
                random_y.append(ng_num)
        else:#第二个以后的reason
            if lastReason==reworkdata[i][0]:#当前reason和上一个reason是同一个reason
                ng_num = ng_num+reworkdata[i][5]#累加不合格数目
                if i == len(reworkdata)-1:#所有循环结束，最后两个reason相同，保存最后一个reason对应的纵坐标
                    random_y.append(ng_num)
            else:                                #当前reason和上一个reason不是同一个reason
                random_x.append(reworkdata[i][0])#保存新的reason
                random_y.append(ng_num)           #保存上一个reason对应的纵坐标，然后初始化成新的reason的ng_num，重新开始累加不合格个数
                ng_num=reworkdata[i][5]          #初始化成新的reason的ng_num
                lastReason = reworkdata[i][0]        #保存最新的reason
                if i == len(reworkdata)-1:#所有循环结束，最后两个reason相同，保存最后一个reason对应的纵坐标
                    random_y.append(ng_num)


    #print("@@@@@@@@@")
    #print(random_x)
    #print(len(random_x))
    #print(random_y)
    #print(len(random_y))

    rework_figure = {
        'data': [
            {'x': random_x, 'y': random_y, 'type': 'bar', 'name': "received product"},
            {'x': 0, 'y': 0, 'type': 'bar', 'name': "finish product"}
        ],

        'layout': {
            'title': 'Rework Status Chart'
        }
    }

    #print("$$$$$$$$$$$$$$$$$$$$$$$$")
    #print(qdata.to_dict('records'))

    reworkTableData = pd.DataFrame.from_records(reworkdata, columns=reworklabel)
    #print(reworkTableData.to_dict('records'))
    return figure_quality, qdata.to_dict('records'),rework_figure,reworkTableData.to_dict('records')
