import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

def plot_category_pie(category_sizes):
    \"\"\"Pie chart for file categories.\"\"\"
    labels = list(category_sizes.keys())
    sizes = list(category_sizes.values())
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.set_title('File Category Breakdown')
    plt.savefig('categories_pie.png')
    plt.close()
    print('Pie chart saved as categories_pie.png')

def plot_top_folders_bar(top_folders, get_size):
    \"\"\"Bar chart for top folders.\"\"\"
    paths = [f[:50] + '...' if len(f) > 50 else f for f, _ in top_folders]
    sizes = [get_size(size) for _, size in top_folders]
    fig, ax = plt.subplots()
    ax.barh(paths, [float(s.replace('GB', '').replace('MB', '')) for s in sizes])  # Simplified
    ax.set_title('Top 10 Folders')
    plt.savefig('top_folders_bar.png')
    plt.close()
    print('Bar chart saved as top_folders_bar.png')

def create_treemap(folder_hierarchy):
    \"\"\"Plotly treemap for folder tree (hierarchy json).\"\"\"
    fig = px.treemap(
        folder_hierarchy,
        path=[px.Constant('root'), 'name', 'children'],  # Adjust based on data
        values='size'
    )
    fig.update_traces(root_color='lightgrey')
    fig.write_html('treemap.html')
    print('Treemap saved as treemap.html (open in browser)')

# Example usage
if __name__ == '__main__':
    # Dummy data
    plot_category_pie({'Videos': 40*1024**3, 'Apps': 30*1024**3, 'Others': 30*1024**3})

