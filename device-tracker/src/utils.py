'''
Utility functions for formatting and updating device data.
'''

def format_battery_percentage(percentage):
    return f"{percentage:.2f}%"

def format_latency(latency):
    return f"{latency:.2f} ms"

def update_graph_data(graph, data):
    graph.clear()
    graph.plot(data['time'], data['battery'], label='Battery Drain', color='blue')
    graph.plot(data['time'], data['latency'], label='Latency', color='red')
    graph.legend()
    graph.draw()