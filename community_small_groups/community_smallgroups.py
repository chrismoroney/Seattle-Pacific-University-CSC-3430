from node import Node
import networkx as graph
import os.path as filepaths
import queue
import sys

###
# get from the user a file of names and size for each group
#   Takes: nothing
#   Returns: ( filename, group_size )
###
def get_user_request():
    filename = str( input( "Please input your plaintext file with the smallgroup names\n" ) )
    while not filepaths.isfile( filename ):
        filename = str( input( "That file does not exist. Please try again:\n" ) )

    group_size_maybe = str( input("\nWhat is the group size? Group size should be no more than half the number of all people. \n") )

    while not group_size_maybe.isdigit()  :
        print( "That wasn't a valid groupsize. Please try again: " )
        group_size_maybe = str( input() )

    group_size = int( group_size_maybe )
    return ( filename, group_size )
# end get_user_request


###
# Read names from a file into a list
#   Takes: filename, a csv file with names
#   Returns: a list of the names in the file
# Names in the list are standard strings
# Married couples are denoted with a +, ie "Mark + Molly"
# Married couples are read in as one name
###
def read_names( filename ):
    try:
        with open( filename ) as people_file:
            all_people = people_file.read()
            # all_people = all_people.replace( "\n", "" )
            people = all_people.split( '\n' )
    except:
        print( "Error reading the file, terminating program." )
        sys.exit()

    # for i in range( len( people ) ):
    #     people[i] = people[i].strip()

    return people
# end read_names


###
# Create a this_graph from a list of names
#   Takes: people, a list of names
#   Returns: A graph with the names as nodes
#            The graph has no edges
###
def create_nodes( people ):
    people_graph = graph.DiGraph()
    for person in people:
        people_graph.add_node( Node( person ) )

    return people_graph
# end create_nodes


###
# make a this_graph with names from a file
#   Takes: filename, a file with the names for the groups
#   Returns: a this_graph with each name as a node
# The this_graph has no edges
###
def setup_graph( filename ):
    people = read_names( filename )
    smallgroups_graph = create_nodes( people )
    return smallgroups_graph
# end setup_graph


###
# get a queue of hosts for the next n weeks (n is number of people in the this_graph)
# Takes:
#   this_graph: the smallgroup this_graph to generate the queue for
#   num_hosts: the number of hosts for each week
# Returns:
#   hosts: the hosts, in the correct order, for the next n weeks
###
def generate_host_queue( this_graph, num_hosts ):
    nodes = list( this_graph.nodes() )
    n = len( nodes )
    hosts = []

    for host_num in range( num_hosts ):
        # create queue
        host = queue.Queue()

        # populate queue
        for i in range( n ):
            # add an offset for each new host so that each week has an appropriate number of DIFFERENT hosts
            host.put( nodes[ ( i + host_num ) % n ])

        # add queue to hosts list
        hosts.append( host )

    return( hosts )
#end generate_host_queue


###
# Add a person to the group
# Takes:
#   current_person: the person to add
#   group: the group to add them to
#   group_sizes: the dictionary with all group sizes for the week
#   this_graph: the smallgroups graph
# Returns: nothing
# modifies group, group_sizes, this_graph
###
def add_person( current_person, group, group_sizes, this_graph ):
    current_host = group[0]
    this_graph.add_edge( current_host, current_person )
    group.append( current_person )
    group_sizes[current_host] += current_person.num_in_household
    return
# end add_person


###
# Do the initial distribution of guests
# Takes:
#   this_graph: the smallgroups graph
#   groups: the list of groups for the week
#   group_sizes: the dict of group sizes that week
#   max_group_size: the max smallgroup size
#   all_people: a queue with every person who isn't a current host
#   already_visited_all: the queue of people who've visited all current hosts
#   need_visit_full: the queue of people who only need visit hosts who are already full
# Returns:
#   Nothing. Modifies this_graph, groups, group_sizes, all_people, already_visited_all, and need_visit_full.
###
def initial_assignment( this_graph, groups, group_sizes, max_group_size, all_people,
                        already_visited_all, need_visit_full ):
    while not all_people.empty():
        next_person = all_people.get()
        placed = False  # whether the person has been assigned to a group
        has_visited_all = True  # whether the person has already visited all the hosts this week

        for group in groups:
            current_host = group[0]
            if not this_graph.has_edge( current_host, next_person ):
                has_visited_all = False
                if ( group_sizes[current_host] + next_person.num_in_household ) <= max_group_size:
                    add_person( next_person, group, group_sizes, this_graph )
                    placed = True
                    break

        if not placed:
            if has_visited_all:
                already_visited_all.put(next_person)
            else:
                need_visit_full.put(next_person)
# end initial_assignment


###
# Make sure all smallgroups have at least the usual number of people
# Takes:
#   this_graph: the smallgroups graph
#   groups: the list of groups for the week
#   group_sizes: the dict of group sizes that week
#   max_group_size: the max smallgroup size
#   already_visited_all: the queue of people who've visited all current hosts
#   need_visit_full: the queue of people who only need visit hosts who are already full
#   catch_all: the queue for collecting leftover people
# Returns:
#   Nothing. Modifies this_graph, groups, group_sizes, already_visited_all, need_visit_full, and catch_all.
# Note:
#   Sometimes because of married couples, one group is (max size + 1) and another is (max size - 1)
###
def fill_as_needed( this_graph, groups, group_sizes, max_group_size, already_visited_all, need_visit_full, catch_all ):
    unfilled_groups = [] # for groups that aren't filled by "visited_all" people
    # fill with people who've visited all the hosts, as much as possible
    for group in groups:
        current_host = group[0]
        while ( not already_visited_all.empty() ) and ( group_sizes[current_host] < max_group_size ):
            next_person = already_visited_all.get()
            add_person(next_person, group, group_sizes, this_graph)
            # group_sizes[current_host] += next_person.num_in_household

        # if there's not enough "visited all" people to fill up this group:
        if group_sizes[current_host] < max_group_size:
            unfilled_groups.append( group )

    # put remaining people into catchall
    while not already_visited_all.empty():
        catch_all.put( already_visited_all.get() )

    # fill groups with people who still need to visit a host, if more fill-in required
    if not ( len( unfilled_groups ) == 0 ):
        for group in unfilled_groups:
            current_host = group[0]
            while( not need_visit_full.empty() ) and ( group_sizes[current_host] < max_group_size ):
                next_person = need_visit_full.get()
                add_person( next_person, group, group_sizes, this_graph )
# end fill_as_needed


###
# Handle any smallgroup fill-in above the max group size
# Takes:
#   this_graph: the smallgroups graph
#   groups: the list of groups for the week
#   group_sizes: the dict of group sizes that week
#   max_group_size: the max smallgroup size
#   need_visit_full: the queue of people who only need visit hosts who are already full
#   catch_all: the queue for collecting leftover people
# Returns:
#   Nothing. Modifies this_graph, groups, group_sizes, need_visit_full, and catch_all.
# Note:
#   If (num_people//max_size), ie the number of hosts, is more than (num_people % max_size), every group will be
#       overfilled by at least one.
###
def do_overfill( this_graph, groups, group_sizes, max_group_size, need_visit_full, catch_all ):
    while not need_visit_full.empty():
        next_person = need_visit_full.get()
        placed = False

        for group in groups:
            current_host = group[0]
            if ( ( not this_graph.has_edge( current_host, next_person ) ) and
                 ( group_sizes[current_host] < ( max_group_size + 1 ) ) ):
                add_person( next_person, group, group_sizes, this_graph )
                placed = True
                break

        if not placed:
            catch_all.put( next_person )

    # distribute any remaining nodes
    if not catch_all.empty():
        for group in groups:
            current_host = group[0]
            next_person = catch_all.get()

            if group_sizes[current_host] < ( max_group_size + 1 ):
                add_person( next_person, group, group_sizes, this_graph )

            if catch_all.empty():
                break
# end do_overfill


###
# Find the smallgroups for one week
#   Takes: this_graph, the current smallgroups this_graph
#          hosts, the hosts for THIS WEEK only
#   Returns: A list of smallgroups
#            Each smallgroup is a list of nodes
###
def get_weekly_group( this_graph, hosts, max_group_size ):
    groups = []
    all_people = queue.Queue() # starts full
    group_sizes = dict() # indexed by host; host:groupsize
    for person in this_graph.nodes():
        if not person in hosts:
            all_people.put( person )

    # queues to deal with nodes that don't initially go into a host
    already_visited_all = queue.Queue() # holds any people who have visited all hosts; starts empty
    need_visit_full = queue.Queue() # holds people who only need to visit full hosts; starts empty
    catch_all = queue.Queue() # distribute last remaining people

    # create a group for each host this week
    for host in hosts:
        groups.append( [host] )
        group_sizes[host] = host.num_in_household

    # initial distribution of groups
    initial_assignment( this_graph, groups, group_sizes, max_group_size, all_people, already_visited_all, need_visit_full )

    # fill up any groups that have empty space
    fill_as_needed( this_graph, groups, group_sizes, max_group_size, already_visited_all, need_visit_full, catch_all )

    # do any possible productive overfill of groups
    if not ( need_visit_full.empty() and catch_all.empty() ):
        do_overfill( this_graph, groups, group_sizes, max_group_size, need_visit_full, catch_all )

    return groups
# end get_weekly_group


###
# Find the smallgroups for each week
# Takes:
#   this_graph: the smallgroup graph
#   group_size: the requested size for each smallgroup
# Returns:
#   The groups for each week:
#   A list containing the groups for each week; each week has a list for each individual groups,
#       and the hosts are the first person in the group list.
###
def get_groups( this_graph, group_size ):
    all_weeks_groups = []
    number_of_people = 0
    for person in this_graph.nodes():
        number_of_people += person.num_in_household

    # find number of hosts based on total number of people and
    # desired group size
    num_hosts = number_of_people // group_size

    # get initial hosts
    hosts = generate_host_queue( this_graph, num_hosts )
    this_week_hosts = [None]*len( hosts ) # unfilled list of size: number of groups

    # set up
    week = 0
    num_households = len( this_graph.nodes() )
    final_num_edges = num_households * ( num_households - 1 )

    # find all groups
    while len( this_graph.edges() ) < final_num_edges: # when the graph is fully connected
        if hosts[0].empty(): # when we run out of hosts, get new ones
            hosts = generate_host_queue( this_graph, num_hosts )

        # get hosts for the week
        for i in range( len( hosts ) ):
            this_week_hosts[i] = hosts[i].get()
            this_week_hosts[i].hosting = True

        all_weeks_groups.append( get_weekly_group( this_graph, this_week_hosts, group_size ) )

        # host nodes cleanup
        for host in this_week_hosts:
            host.hosting = False

        week += 1

    return all_weeks_groups
# end get_groups


###
# output the smallgroups into a file
# Takes: all_weeks_groups, a list containing the smallgroups for each week.
#   See header of get_groups for details about list structure
# Returns: nothing
def output_results( all_weeks_groups ):
    with open( "smallgroups.txt", 'w' ) as groups_file:
        groups_file.write( "SMALLGROUP ASSIGNMENTS:")
        week_num = 1
        for week in all_weeks_groups:
            groups_file.write( "\nWEEK " + str( week_num ) + '\n' )
            group_num = 1
            for group in week:
                groups_file.write( "GROUP " + str( group_num ) + ': ' )
                for person in group:
                    if person == group[0]:
                        groups_file.write( str( person) + " (hosting) | " )
                    elif person == group[len(group) - 1]:
                        groups_file.write( str( person ) + '\n')
                    else:
                        groups_file.write( str( person ) + " | " )
                group_num += 1
            week_num += 1

    print( "See smallgroups.txt for your smallgroup assignments.")
    return
# end output_results


###
# master function for getting smallgroups
# Takes: nothing
# Returns: nothing
###
def run_smallgroups():
    filename, num_hosts = get_user_request()
    groups_graph = setup_graph( filename )
    all_weeks_groups = get_groups( groups_graph, num_hosts )
    output_results( all_weeks_groups )
# end run_smallgroups

### end function declarations ###

run_smallgroups()