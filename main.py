

# MAIN PROGRAM
# handling the interaction with the user
# 
#
# TO DO FOR MAIN:
# - Add description of the main somewhere here 
# - Add specific airport based on name 
# - Add a plot of the top .. airlines that will be selected, like in airports (so you see which airlines it will plot)
# - Add inspect module and options
# - Check consistency, does it print 'you chose ..' everywhere, and is there a default variable when the right option is not chosen?
# - Put demo + programm option 2 into module
# - Adding comments
# - Write some code shorter


#%% Import modules and packages

# self-defined modules
import base_preprocessing as bpp
import module_visualization_worldmap as worldmap
import module_comparison as comp
import module_inspect_data as inspect
import module_comparison_airlines as comp_air

# other modules
import networkx as nx

# list of other packages to install:
# matplotlib
# pandas
# numpy
# networkx
# basemap
# operator


#%% Load data

# define filenames which you want to load
# in this case a csv with all flight routes and a csv with geographical locations of airports
filename_routes = "routes.csv"
filename_airports = "airports-extended.csv"
filename_airlines = "airlines.txt"

# load flight routes data into dataframe
try:
    df_routes = bpp.load_data_routes_from_file(filename_routes)
except FileNotFoundError:
    print("file not found, please check filename_routes and current directory")
except Exception as err: 
    print("Something went wrong")
    print(err)

# load airports data into dataframe    
try:
    df_airports = bpp.load_data_airports_from_file(filename_airports)
except FileNotFoundError:
    print("file not found, please check filename_routes and current directory")
except Exception as err: 
    print("Something went wrong")
    print(err)   
    
# load airlines data into dataframe    
try:    
    df_airlines = bpp.load_data_airlines_from_file(filename_airlines)
except FileNotFoundError:
    print("file not found, please check filename_routes and current directory")
except Exception as err: 
    print("Something went wrong")
    print(err) 
    
    
#%% Preprocessing: merging and cleaning of dataframes
    
### MAYBE PUT ALL IN PREPROCESSING WITH METAFUNCTION

# left outer join of routes and airlines dataframes
df_merge_airlines_info = bpp.left_merge_dataframes(df_routes, df_airlines, "airline ID")

# left outer join of routes and airports dataframes
df_merged = bpp.left_merge_dataframes(df_merge_airlines_info, df_airports, "source airport ID")

# reindex columns of dataframe
df_merged = df_merged.reindex(columns=["airline IATA code", "airline ID", "name airline", "country airline", "source airport", "source airport ID", "destination airport", "destination airport ID", "airport name", "airport city", "airport country", "latitude", "longitude"])

# cleaning of the merged dataframe
df_merged = bpp.clean_dataframe(df_merged)   


#%% Run program in loop until user chooses to exit

while True:   
# print options to user:
    choice = input("""What do you want to do?
    0\tSee demo visualization of the flight network.
    1\tInspect the dataframes               
    2\tVisualise flight network with self-chosen parameters.
    3\tCompare airlines.
    4\tExit program.
    enter answer (0/1/2/3/4): """)
    
    # set default variables for the visualisation
    dataframe = df_merged
    directionality = nx.Graph()
    node_size = 20
    node_visibility = 0.8
    edge_visibility = 0.1
    
    # evaluate user choice and proceed accordingly
    if choice == "0": # see demo
        
        demo_options = input("""What do you want to do?
        1\tShow both airports and flight routes             
        2\tShow only airports
        3\tShow only flight routes
        enter answer (1/2/3): """)
        if demo_options == '1':
            print('You chose to show both airports and flight routes')
        elif demo_options == '2':
            print('You chose to show only the airports')
            edge_visibility = 0
        elif demo_options == '3':
            print('You chose to show only the flight routes')
            node_visibility = 0
        else:
            print('Sorry, this is not an option, we will use the default setting')  
            
        # visualize demo flight network    
        worldmap.visualize_on_worldmap(dataframe, directionality, node_size, node_visibility, edge_visibility)
    

    elif choice == "1": # Inspect data

        inspect.inspect_data(df_routes, df_airports, df_merged)
    
    elif choice == "2": # Visualize flight network
        
        # 1st parameters: amount of airlines and airports
        map_amount = input("""What do you want to do?
        1\tSelect all airlines and airports              
        2\tSelect specific airlines
        3\tSelect specific airports
        enter answer (1/2/3): """)
        
        if map_amount == '1':
            print('You chose to plot all airlines and airports')
              
        
        elif map_amount == '2':
            print('You chose to plot specific airlines')
            choice_airlines = input("""What do you want to do?
            1\tSelect the biggest airlines             
            2\tSelect a specific airline
            enter answer (1/2): """)
            
            if choice_airlines == '1':
                print('You chose to plot the biggest airlines')
                map_number_airlines = int(input('How many of the biggest airlines do you want to plot? (1 to 50) '))
                
                if 1 <= map_number_airlines <= 50:
                    print(f'You chose to plot the top {map_number_airlines} biggest airlines')

                    #create a table with the top airlines with n. of flights
                    airline_table = comp.airline_table(df_merged)

                    #dataframe with the flights of the desired n.of airlines 
                    unadjusted_dataframe=comp.take_nairlines(df_merged, airline_table, map_number_airlines)
                    #clean the dataframe to have the position of every airport to plot nicely
                    dataframe = bpp.clean_dataframe(unadjusted_dataframe)
                     # show barplot of amount of flight routes (edges) per hub airport
                    comp.barplot_airlines(df_airlines)
            

                    
                    # create a dataframe with only the flights of the selected airlines
                    dataframe = comp.take_nairlines(df_merged, airline_table, map_number_airlines)
                    
                    # take top n rows of table specifief by number
                    top_table = airline_table[:map_number_airlines]
                    
                    # show barplot of amount of flight routes per airline
                    comp.barplot_from_df(top_table, x="airline IATA code" , y="flight_routes_nr" , ylabel="flight routes")
                    

                else:
                    print('Sorry, this is not an option, we will use the default setting') 
                    
            elif choice_airlines == '2':   
                print('You chose to plot a specific airline based on name')
                
                # create a dataframe with only the in- and outcoming flights of the selected airport through user
                dataframe = comp.define_airline_through_user_input(df_merged)
                
            
            
        elif map_amount == '3':
            print('You chose to plot specific airports')
            choice_airports = input("""What do you want to do?
            1\tSelect the biggest airports             
            2\tSelect a specific airports
            enter answer (1/2): """)  
            
            if choice_airports == '1':
                print('You chose to plot the biggest airports')
                map_number_airports = int(input('How many of the biggest airports do you want to plot? (1 to 50) '))
                if 1 <= map_number_airports <= 50:
                    hubs_nr = map_number_airports
                    print(f'You chose to plot the top {hubs_nr} biggest airports')
                
                    # determine what are the top 'n' most connected airports (hubs)
                    hub_table = comp.find_hubs_in_df(df_merged, hubs_nr)
                
                    # create a dataframe with only the in- and outcoming flights from hub airports
                    df_hubs = comp.hub_network_df(df_merged, hub_table)
                
                    # show barplot of amount of flight routes (edges) per hub airport
                    comp.barplot_from_df(hub_table, x="airport" , y="degree", ylabel="flight routes")
                else:
                    print('Sorry, this is not an option, we will use the default setting') 
                    
            elif choice_airports == '2':
                print('You chose to plot a specific airport based on name')
                
                # create a dataframe with only the in- and outcoming flights of the selected airport through user
                dataframe = comp.define_airport_through_user_input(df_merged)

            # comment Jaap: I think we can write a lot of things way cleaner, such as the lines above
            # these could go in on scentince: dataframe = bpp.clean_dataframe(comp.specific_airport_df(dataframe,airport))
            # comment Kirsten: for now i thought it would be better to include cleaning function into the creating the df function, so that's cleaner already;)
 
        else:
            print('Sorry, this is not an option, we will use the default setting')                  
    
    
        # 2nd parameter: directed or undirected network
        map_edges = input("""What do you want to do?
        1\tMake an undirected network              
        2\tMake a directed network
        enter answer (1/2): """)
        
        if map_edges == '1':
            print(f'You chose to create an undirected network')
            
        elif map_edges == '2':
            print(f'You chose to create a directed network')
            directionality = nx.DiGraph()
            
        else:
            print('Sorry, this is not an option, we will use the default setting')   
        

        # 3rd parameter: size of the airports
        size_airport = input("""What do you want to do?
        1\tDisplay all airports with the same size             
        2\tDisplay size of airport depending on how many flight routes it has (degree)
        enter answer (1/2): """)
        
        if size_airport == '1':
            print('You chose to display all airports with the same size')
            
        elif size_airport == '2':
            print('You chose to display airport size dependent on degree')
            
            # create graph object from dataframe defined as 1st parameter
            graph = comp.create_graph_object(dataframe)
            
            # ADJUST! now degree of node changes dependent on subnetwork.
            # degree should be static, based on whole network!
            # use graph object to calculate degree per node and write to list
            node_size = comp.node_size_degree(graph)
            
        else:
            print('Sorry, this is not an option, we will use the default setting')
        
        
        # VISUALIZE FLIGHT NETWORK WITH USER OPTIONS
        worldmap.visualize_on_worldmap(dataframe, directionality, node_size, node_visibility, edge_visibility)
     
            
    elif choice == "3": # THIS IS FOR THE COMPARISON
        print("You chose to compare airlines")
        
        # let user specify airlines to visualize and create dataframes for both 
        df_airline1 = comp.define_airline_through_user_input(df_merged)
        print("You choose your first airline. Now select another one to compare!")
        
        df_airline2 = comp.define_airline_through_user_input(df_merged)
        
        # visualize airline networks on worldmap
        comp_air.visualize_two_networks_on_worldmap(df_airline1, df_airline2)  
        
        # print network metrics table
        comp_air.create_graph_metrics_table(df_airline1, df_airline2)
                
        
    elif choice == "4": # Exit program 
        print("Thank you for using this program.")
        break 
    
    else:
        print("Choice not recognized. Try again.")
        
        
        
      
    
