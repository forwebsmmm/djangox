from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import GeoPoints
from django.urls import reverse_lazy 

# Create your views here.
import osmnx as ox
import networkx as nx
import folium


class RoutesListView(ListView):
    model = GeoPoints
    template_name = 'routes_list.html'
    

class RouteShowView(DetailView):
    model = GeoPoints
    fields = ('route_name',)
    template_name = 'show_route.html'
    
    # def get_context_data(self, **kwargs):
    #     obj = self.get_object()
    #     ox.config(log_console=True, use_cache=True)

    #     G = ox.graph_from_place('Sievierodonetsk, UA', network_type='drive')

    #     a = (48.946406, 38.50163)
    #     b = (48.949788, 38.484678)

    #     orig_node = ox.get_nearest_node(G, a, method='euclidean')
    #     dest_node = ox.get_nearest_node(G, b, method='euclidean')

    #     route_direct = nx.shortest_path(G, orig_node, dest_node, weight='length')
    #     route_return = nx.shortest_path(G, dest_node, orig_node, weight='length')

    #     route_map = ox.plot_route_folium(
    #         G, route_direct, route_color='green', route_width=5, route_opacity=0.5, tiles='openstreetmap', popup_attribute='length')
    #     route_map = ox.plot_route_folium(
    #         G, route_return, route_color='blue', route_width=5, route_opacity=0.5, route_map=route_map, popup_attribute='length')
    #     folium.Marker(location=(G.node[orig_node]['y'], G.node[orig_node]['x']),
    #                 icon=folium.Icon(color='green', prefix='fa', icon='flag')).add_to(route_map)
    #     folium.Marker(location=(G.node[dest_node]['y'], G.node[dest_node]['x']),
    #                 icon=folium.Icon(color='blue', prefix='fa', icon='flag-checkered')).add_to(route_map)

    #     context = super().get_context_data(**kwargs)
    #     context['generated_route'] = HttpResponse(route_map.get_root().render())
    #     return context

class RouteCreateView(CreateView):
    model = GeoPoints
    template_name = 'geopoint_new.html'
    fields = ('route_name', 'point_a', 'point_b', 'point_c', 'point_d')
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # obj = self.get_object()
        ox.config(log_console=True, use_cache=True)

        G = ox.graph_from_place('Sievierodonetsk, UA', network_type='drive')

        a = (form.instance.point_a, form.instance.point_b)
        b = (form.instance.point_c, form.instance.point_d)

        orig_node = ox.get_nearest_node(G, a, method='euclidean')
        dest_node = ox.get_nearest_node(G, b, method='euclidean')

        route_direct = nx.shortest_path(G, orig_node, dest_node, weight='length')
        route_return = nx.shortest_path(G, dest_node, orig_node, weight='length')

        route_map = ox.plot_route_folium(
            G, route_direct, route_color='green', route_width=5, route_opacity=0.5, tiles='openstreetmap', popup_attribute='length')
        route_map = ox.plot_route_folium(
            G, route_return, route_color='blue', route_width=5, route_opacity=0.5, route_map=route_map, popup_attribute='length')
        folium.Marker(location=(G.node[orig_node]['y'], G.node[orig_node]['x']),
                    icon=folium.Icon(color='green', prefix='fa', icon='flag')).add_to(route_map)
        folium.Marker(location=(G.node[dest_node]['y'], G.node[dest_node]['x']),
                    icon=folium.Icon(color='blue', prefix='fa', icon='flag-checkered')).add_to(route_map)
        generated_route = route_map.get_root().render()
        form.instance.route_view = generated_route
        return super().form_valid(form)


def mapShow(request, **kwargs):
    route_id = kwargs['pk']
    route = GeoPoints.objects.get(id=route_id)
    route_map = route.route_view
    return HttpResponse(route_map)