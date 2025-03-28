import networkx as nx  # type: ignore
import plotly.graph_objects as go  # type:ignore
import matplotlib.pyplot as plt  # type: ignore

# source: https://lopezyse.medium.com/make-interactive-knowledge-graphs-with-python-cfe520482197

def get_edges():
    edges = [
        ('drugA', 'fever', {'label': 'treats'}),
        ('drugB', 'hepatitis', {'label': 'treats'}),
        ('drugC', 'bleeding', {'label': 'treats'}),
        ('drugD', 'pain', {'label': 'treats'}),
        ('drugA', 'gene1', {'label': 'inhibits'}),
        ('drugC', 'gene2', {'label': 'inhibits'}),
        ('drugD', 'gene4', {'label': 'inhibits'}),
        ('drugE', 'gene20', {'label': 'inhibits'}),
        ('gene1', 'obesity', {'label': 'associated'}),
        ('gene2', 'heart_attack', {'label': 'associated'}),
        ('gene3', 'hepatitis', {'label': 'associated'}),
        ('gene4', 'bleeding', {'label': 'associated'}),
        ('gene50', 'cancer', {'label': 'associated'}),
        ('gene2', 'gene1', {'label': 'associated'}),
        ('gene3', 'gene20', {'label': 'associated'}),
        ('gene4', 'gene50', {'label': 'associated'}),   
    ]
    return edges

def create_edge_traces(G: nx.Graph, pos):
    edge_traces  = []  # type:ignore
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=0.5, color='gray'),
            hoverinfo='none'
        )
        edge_traces.append(edge_trace)
    return edge_traces 

def create_node_trace(G: nx.Graph, pos, color: str = 'lightblue'):
    x = [pos[node][0] for node in G.nodes()]
    y = [pos[node][1] for node in G.nodes()]
    text = [node for node in G.nodes()]
    node_trace = go.Scatter(
        x=x, y=y, text=text,
        mode='markers+text',
        marker=dict(size=10, color=color),
        textposition='top center',
        textfont=dict(size=7),
        hoverinfo='text',
    )
    return node_trace

def create_edge_label_trace(G: nx.Graph, pos):
    x = [(pos[edge[0]][0] + pos[edge[1]][0]) / 2 for edge in G.edges()]
    y= [(pos[edge[0]][1] + pos[edge[1]][1]) / 2 for edge in G.edges()]
    text = [G[edge[0]][edge[1]]['label'] for edge in G.edges()]
    edge_label_trace = go.Scatter(
        x=x, y=y, text=text,
        mode='text',
        textposition='middle center',
        textfont=dict(size=7),
        hoverinfo='none'
    )
    return edge_label_trace

def create_layout():
    layout = go.Layout(
        title='Example Graph with plotly',
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis_visible=False,
        yaxis_visible=False
    )
    return layout

def create_figure(G: nx.Graph, pos) -> go.Figure:
    edge_traces = create_edge_traces(G, pos)
    node_trace = create_node_trace(G, pos)
    edge_label_trace = create_edge_label_trace(G, pos)
    layout = create_layout()
    fig = go.Figure(
        data=edge_traces + [node_trace, edge_label_trace],
        layout=layout
    )
    return fig
    

def main(is_plt: bool):
    G = nx.Graph()
    edges = get_edges()
    G.add_edges_from(edges)
    # pos = nx.fruchterman_reingold_layout(G, k=0.5, seed=127)
    # note:  kamada takes more time but repect the underlying structure
    # and is deterministic
    pos = nx.kamada_kawai_layout(G)
    if is_plt:
        nx.draw(G, pos=pos, with_labels=True, font_weight='bold')
        plt.show()
    else:
        fig = create_figure(G, pos)
        fig.show()

if __name__ == "__main__":
    main(is_plt=False)

