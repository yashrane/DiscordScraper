# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


#dark theme
colors = {
    'background': '#23272A',
    'text': '#7289DA',
	'foreground':'#2C2F33'
}

#light theme
# colors = {
	# 'background':'white', 
	# 'text':'black'
# }

df = pd.read_csv("../plots/lib/messages.csv", names=['Roles', 'Timestamp', 'Channel', 'Content', "User ID", "Toxicity"], parse_dates=[1])

df['Regular'] = df['Roles'].str.contains("Regular")
df['Mapachito'] = df['Roles'].str.contains('Mapachito')
df['Timestamp'] = df['Timestamp'].dt.tz_localize('UTC').dt.tz_convert("America/Los_Angeles")

last_timestamp = df.iloc[len(df)-1]['Timestamp']
pastday = df[df['Timestamp'].between(last_timestamp.floor('D'), last_timestamp)]

def usage_info():
	df['Month'] = df['Timestamp'].dt.month

	reg_table = df.groupby("User ID").agg({
			'Month': pd.Series.nunique, 
			"Content": pd.Series.count,
			"Regular": any, 
			"Mapachito": any
			})
	reg_table['Count'] = reg_table['Content']/reg_table['Month']

	#AddThreshold = reg_table[reg_table['Regular']]['Count'].mean()
	AddThreshold = reg_table['Count'].mean()

	#RemoveThreshold = reg_table['Count'].mean()
	RemoveThreshold = reg_table[reg_table['Regular'] == False]['Count'].mean()

	add_list = reg_table[(reg_table['Regular'] == False) & (reg_table['Count'] > AddThreshold)]
	remove_list = reg_table[reg_table['Regular'] & (reg_table['Count'] < RemoveThreshold)]
	
#	return add_list['User ID'], remove_list['User ID']
	return add_list.index, remove_list.index



def dropdown(title, elements, title_color='white',color='white'):
	children = []
	for e in elements:
		children.append(html.P(e))
	
	
	return card(
		html.Div(children=[
			html.Div(html.H4(title, 
			style={
				'textAlign': 'center',
				'color': title_color, 
			}),
			style={'background-color':colors['foreground']}),
			html.Div(
				children=children, 
				style={
					'color':color,
					'padding':'10px'
			})], 
			style={'background-color':'#36393e'}
		),
		width='70%')
	
	
	
	

def notifications():

	add_list = ["Pichuu", 'Purity', "Josephine"]
	remove_list = ["Moejoe", "chanel"]

	#add_list, remove_list = usage_info()
	problem_users = ["Moose", "Oppen"]
	new_users = ['burnt', 'GreatGuy']
	
	
	
	
	return html.Div(
			children=[
				dropdown("Problem Users", problem_users, '#e74c3c'),
				dropdown("Pending Introductions", new_users, colors['text'], 'white' ),
				dropdown("New Regulars",add_list,colors['text'], 'white'), 
				dropdown("New Regulars Mortis", remove_list, colors['text'], 'white')
			], 
			style={
				'height':'100%',
				'width':'40%', 
				'display':'inline-block', 
				'vertical-align':'top', 
			})
	
	
def interpolate(hours, counts):
	i=1
	while i < len(hours):
		if hours[i]-hours[i-1] != 1:
			hours.insert(i, i)
			counts.insert(i,0)
		i=i+1
	return hours,counts
	
def to_time(hours):#TODO: need some interpolation here to deal with values that are missing
	times = []
	for h in hours:
		if h>0 and h <= 11: #1am-11am
			times.append(str(h)+"AM")
		elif h >12 and h <= 23: #1pm-11pm
			times.append(str(h-12)+"PM")
		elif h == 0: #12am
			times.append('12AM')
		else:#12pm 
			times.append('12PM')
	return times
	

def usage_plot():
	#look at the toxicity per channel, if some channel is unusually toxic, create notifications
	
	
	counts = pastday.groupby(pastday['Timestamp'].dt.hour)['Timestamp'].count()


	print(counts.index)
	hours, counts = interpolate(list(counts.index), list(counts))
	print(hours)
	hours = to_time(hours)
	print(hours)
	
	return dcc.Graph(
			id='usage-graph',
			figure={
				'data': [
					{'x': hours, 'y': counts, 'type': 'scatter', 'name': 'SF'},
#					{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
				],
				'layout': {
					'plot_bgcolor': colors['foreground'],
					'paper_bgcolor': colors['foreground'],
					'font': {
						'color': colors['text']
					},
					'title': 'Activity Today', 
					'y-axis':{'title':'# of Messages'}
				}
			}, 
			style={
				'height':'30%',
				'width':'100%'
			}
		)
		
def toxicity_plot():
	
	avg_day = df.groupby(df['Timestamp'].dt.day)['Toxicity'].mean().mean()
	past_day_toxicity = pastday['Toxicity'].mean()
	percent_increase = (past_day_toxicity-avg_day)/avg_day
	
	
	
	return dcc.Graph(
			id='toxic-chart',
			figure={
				'data': [
					{
						'values':[past_day_toxicity, 1-past_day_toxicity], 
						'type': 'pie', 
						'name': 'toxicity', 
						"hole": .4,
						'marker':{'colors':[colors['text'], colors['foreground']]},
						'textinfo':'none'
					}
				],
				'layout': {
					'showlegend':'false',
					'plot_bgcolor': colors['foreground'],
					'paper_bgcolor': colors['foreground'],
					'font': {
						'color': colors['text']
					},
					'title':'Average Toxicity Today' , 
					'annotations': [
						 # {
							# "font": {
								# "size": 20
							# },
							# "showarrow": False,
							# "text": "Up " + str(str(round(percent_increase*100, 1))) + "% from yesterday",
							# # "x": 0,
							# # "y": 0, 
							# # 'textposition':'bottom center'
						 # }, 
						{
							"font": {
								"size": 30
							},
							"showarrow": False,
							"text": str(round(past_day_toxicity*100, 1))+"%",
							# "x": 0,
							# "y": 0, 
							# 'align':'center'
						}
						]
				}
			}, 
			style={
				# 'height':'50%',
				 # 'width':'50%', 
				# 'display':'inline-block'
				# 'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
				# 'transition': '0.3s'
			}
		)
		

def card(content, width='100%', height='100%'):
	return html.Div(children=[
		html.Div(
		children=content, 
		style={
			'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
			'transition': '0.3s',
			'width':width,
			'height':height,
			'margin':'auto', 
			# 'display':'inline-block', 
			# 'align':'center'
		}), 
		html.Div(style={'padding':'5px'})]
		)



app = dash.Dash()



app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Discord Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # html.Div(children='Dash: A web application framework for Python.', style={
        # 'textAlign': 'center',
        # 'color': colors['text']
    # }),

	html.Div(children=[
	
		notifications(), 
	
		html.Div(children=[
				card(usage_plot(), height='30%'), 
				card(toxicity_plot(), width='50%', height='70%')
			], 
			style={
				'width':'60%', 
				'display':'inline-block'
			}
		)
	
	])
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


if __name__ == '__main__':
    app.run_server(debug=True)