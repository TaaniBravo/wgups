# B1. Overview
WGUPS need to determine an efficient route and delivery distribution because the current system in place is not delivering packages before their deadline. This is the main requirement of this algorithm although another requirement is that the accumulative miles to deliver all the packages need to be less than 140 between all 3 trucks.

Algorithm Overview:

The algorithm chosen for this Python script is the nearest neighbor (NN) algorithm. This was chosen for a few reasons:
1.	The simplicity of the algorithm. Nearest neighbor is extremely easy to implement and considering the graph of the map is complete meaning that every location connects to every other location means we can narrow our destinations down to where the packages on a truck are and pick the closest location to our current location until we’ve delivered everything.
2.	Another is the adaptability of nearest neighbor. It’s very easy to implement this algorithm into another city and have it be effective.
3.	The next is the scalability of the algorithm remains stable even when WGUPS scales to larger scaled cities. This is because the algorithm handles locations in a dynamic fashion and no predetermined route is needed.

Now that we have gone over the reason for choosing the nearest neighbor algorithm, I can explain how we implemented it. There’s dynamic logic surrounding the core NN algorithm but the core algorithm is a very simple O(N) time complexity function.
```
Pseudocode leading up to Nearest Neighbor Algorithm.

Read data from CSV files for locations, packages, and distances.

Initialize our trucks and drivers.

Load our trucks with packages.

Truck 1 is loaded and leaves early at 8:00 AM to deliver many of the packages with an early deadline.
Truck 2 is loaded and leaves at 9:05 AM to deliver the rest of the packages that might have a deadline but are delayed.
Truck 3 is loaded and awaits to leave once a driver becomes available.

Nearest Neighbor Algorithm O(n) time complexity.
while there are addresses that we need to deliver to
    find the closest address in the truck's list to deliver, to our current location
    deliver the package(s) to the address
    update our current location
    update the accumulated miles and the time spent traveling
    remove the location from address that we need to deliver to
```

# B2. Programming Environment
```commandline
IDE: Pycharm
Version: Python 3.10.0
OS: Windows 11 Intel i9
```

# B3. Scalability & Adaptability
Like mentioned in the overview of why I chose the NN algorithm. 
The algorithm is very scalable and adaptable. 
This is because the algorithm is dynamic and doesn’t need a predetermined delivery route. 
This means that if WGUPS changes to a different city, the algorithm will still be effective. 
The only thing that would need to be changed is the map of the city and the locations of the packages. 
It is important to note thought the way the trucks are loaded would also need to be changed
as I chose for the sake of time to not implement dynamic loading (although it's very easy to add a new list 
of package IDs we need to deliver. 
If we were to productionize the product I would want to make sure that we define that
in the requirements everything besides the data that is operated on should be automatic.

# B4. Architecture
The architecture of the script very easy to follow and iterate over to improve. There is the src folder which contains the main.py which fires everything off and then in the lib folder we have the following:
```
main.py - File to run the program
lib
├───__init__.py - Contains the index for the lib folder
├───ChainingHashTable.py - Contains the ChainingHashTable class
├───constants.py - Contains constant values
├───Driver.py - Contains the Driver class
├───DriverPool.py - Contains the DriverPool class
├───Graph.py - Contains the Graph class
├───UI.py - Contains the UI class
├───Location.py - Contains the Location class
├───Package.py - Contains the Package class
├───Truck.py - Contains the Truck class
└───TruckPool.py - Contains the TruckPool class
```

# B5. Efficiency and Maintainability
The efficiency of the script is very good for the requirements of this service. 
Both the time and space complexity of the core algorithm is O(N). 
This is a result of us keeping a list of addresses that we need to deliver to and iterating
over that list until it's empty and the packages are delivered.

The maintainability of the program is easy to maintain as well because of the simple architecture
provided in the previous section and the fact that the to deliver more packages you just need to update
the list of package IDs that get loaded into the truck.

# B6. Strengths and Weaknesses
The strengths of the HashTable that was created to store the Downtown Map route distances
and adjacency list are very solid because they are essentially a Python dictionary.
They provided the exact support I need to handle the data for the distance.csv and making sure that
I can store the locations as keys with value being the distance to the other locations.

The weakness of the HashTable that was implemented was that with the bucket implementation
(to avoid collisions) that means we can potentially run O(N) time complexity on the get and set method.

# D1. HashTable Implementation
The HashTable implementation is a Chaining HashTable. This means that we have a list of buckets.
Each bucket contains a list of key value pairs. The key is a tuple of the "from" location and the 
"to" location and the value is the distance. This is used by the NN algorithm chosen by 
determining the nearest location to the current location in the hash table.

# I1. Strenths of Nearest Neighbor Algorithm
The strengths of the NN algorithm is that it's very easy to implement and that it's time complexity is O(N).

The algorithm in the solution meets the requirements to deliver all the packages before their deadline
and also make sure that they are delivered in a very efficient manner.

There are two other implementations that I considered for this solution.
The first was a greedy algorithm where we just pick the next location in our list of locations.
This would have been very simple but not very efficient. 
The second was using Dijkstra's algorithm which would have been very efficient but would have been
overkill for the requirements of this solution. This is because the graph is complete, and we don't need
to find the shortest path to a location. We just need to find the nearest location to our current location.

# J. What would I do differently?
If I had more time I would have implemented the dynamic loading of the trucks. This would make the program far more 
useful for other companies outside WGUPS. I would also have implemented a UI that would allow the user to
more visuals on the program. And real time updates on the status of the trucks and the packages.