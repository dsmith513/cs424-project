#### Task 1: Observation and data collection plan

The data that I have collected is passenger data for the train rides that I take on my commute to and from UIC every day. I take the UP-NW Metra line from Cary to Chicago OTC. Depending on the day of the week, the inbound and outbound trains that I take are different. I will be recording how many passengers enter and exit the train car that I am in at each stop during my commute. Each individual train ride counts as one observation. I will be recording multiple different attributes for each observation. I will be recording the date, day of the week, train number, departure time, existing passengers prior to me getting on the train, how many passengers get on and off at each stop, and the total passengers left at the final stop. So far I have recorded data over a two week period from 9/21 to 10/1. This means that I have observations spanning over 10 days with a total of 2 observations per day (1 inbound and 1 outbound observation) totaling 20 observations. Additional observations can easily be collected as the semester continues. There exists meaningful variation among the locations, dates, and times of the data collected. I take the 8:24 AM inbound train and the 12:35 PM outbound train on Monday, Wednesday, and Friday. I take the 7:54 AM inbound train and the 5:15 PM outbound train on Tuesday and Thursday. There are 18 possible stops for each train between Cary and Chicago OTC. Four different trains will be observed, and not every train stops at all 18 stops. For example, the 5:15 PM outbound train is express from Chicago OTC and only stops at Palatine, Barrington, and Fox River Grove before I get off at Cary. Since I am working alone, all of the data collection was done by me. The current data collection process fails to capture passenger data outside of the stops observed by my commute. Each observed train has additional stops past Cary that are not able to be observed. Additionally, I am only able to observe the passenger data for the train car that I am in. Each train has multiple cars and it is not possible for me to be in all of them at once. One aspect of the data collection process that could introduce bias is the limited sampling window. So far, I have only had two weeks to collect the data. It is plausible that this limited sampling window will result in bias that would otherwise not be present if I were able to record samples over a longer period of time. The different stop schedules of each train may also introduce bias. The blank entries in the dataset indicate that the train did not stop at that station. If these entries were treated as zeroes, comparisons would be distorted.

Four Domain Questions:

1. How do passenger boarding and exiting counts vary across stations?

2. How does the number of passengers on the train change along the route, and where is occupancy highest?

3. How do passenger volumes differ between inbound and outbound trips?

4. How do boarding, exiting, and occupancy patterns vary by weekday and train service?

The data dictionary is located in data-dictionary.md

#### Task 2: Pilot and data collection

The pilot collection consists of the first ten train rides observed. These were observed from Monday 9/21 to Friday 9/25. Two train rides were observed each day for a total of ten (one inbound and one outbound each day). The observations were not difficult to classify. Classifying whether I was on an inbound or an outbound train was obvious. Sometimes, particularly on the express trains, it was difficult to record how many passengers were getting on and off the train at a particular stop. The most difficult stop to record is Palatine during the 5:15 PM outbound train. Because so many passengers are exiting at this stop, recording accurate counts can sometimes be difficult. It is entirely possible that there are some slightly inaccurate entries in the existing data. Some attributes are missing depending on the train observed. Not every train stops at every station, so some attributes are intentionally left blank. Some of the recorded attributes are redundant. The train number and departure time are technically recording the same information, but I have chosen to leave both in for the sake of completeness.

#### Task 3: Data description and domain questions

The data collected currently shows the passenger data from my commutes to and from UIC from the period of 9/21 to 10/2. The data was recorded by me during my commute, and contains temporal variation based on which train I took to and from UIC on the particular day it was recorded. The specific trains recorded were selected based on what time my first class starts and what time my last class ends on each particular day. For example, on Tuesdays and Thursdays my first class is CS 424. CS 424 starts at 9:30 so I take train 638 which departs Cary at 7:54 to ensure I make it to class on time. There were limitations to the data that I was able to collect. As was mentioned earlier, I am only able to ride one train at a time and am only able to record the passenger data for the train car that I am physically located in. These physical limitations could potentially introduce bias in the data. I discussed earlier that sometimes the passenger data was difficult to record when there were a lot of passengers entering or exiting at the same stop. This was particularly true on express trains that visited fewer stops. Generally speaking, the more passengers that got on or off at a particular stop, the more difficult it was to accurately record the appropriate counts. When making the observations, I recorded the number of passengers that got on or off at a particular stop using the notes app on my phone. I was then able to transcribe those values into an Excel spreadsheet and total them to get an accurate total for how many passengers total either got on or off at Chicago OTC. 

Domain Questions from Task 1:

1. How do passenger boarding and exiting counts vary across stations?

2. How does the number of passengers on the train change along the route, and where is occupancy highest?

3. How do passenger volumes differ between inbound and outbound trips?

4. How do boarding, exiting, and occupancy patterns vary by weekday and train service?

I will be moving forward with domain questions 1, 2, and 4 from Task 1 during the visualization stages. These questions do not need to be revised after the data collection process. Question 1 is the most straightforward. Investigating the different counts of passenger boarding across each station is a good starting point for the visualizations. Question 2 investigates how the total number of passengers changes along the train route as well as where occupancy is the highest. The occupancy portion of Question 2 will apply more to the outbound trains, as the inbound trains are likely to have the highest occupancy at the final stop Chicago OTC. Question 4 analyzes passenger data variation based on weekday. This is a good question to include because many commuters don't need to go into the office every day. Many office workers now have hybrid work schedules meaning that they work from home some days of the week. This affects the passenger data on each weekday and makes Question 4 an interesting inclusion. I have decided to replace Question 3 with a more interesting domain question: How do passenger volumes differ between express and non-express trains? I believe that this revised Question 3 will provide more interesting visualization and analysis. I currently am recording observations for express and non-express trains, so having a question designed to compare them will be good.

Revised Domain Questions:

1. How do passenger boarding and exiting counts vary across stations?

2. How does the number of passengers on the train change along the route, and where is occupancy highest?

3. How do passenger volumes differ between express and non-express trains?

4. How do boarding, exiting, and occupancy patterns vary by weekday and train service?

#### Task 4: Task abstractions

1. How do passenger boarding and exiting counts vary across stations?
    Actions: Compare, rank, and identify extremes
    Targets: Boarding and exiting counts grouped by location, with trip direction and service as context
    Abstract Task: Compare two quantitative measures across locations and identify locations with unusually high or low values.

I mapped Domain Question 1 to comparison because its main goal is to understand differences between stations. Ranking and identifying extremes make that goal more specific: a user should be able to determine which locations have the most boarding or exiting activity. Boarding and exiting are separate targets because a station may have high counts for one action and low counts for the other. When summarizing multiple trips, average counts per observed stop allow comparisons without favoring stations that were visited more often. Skipped stops should be excluded from those averages rather than counted as zero. This abstraction shifted my focus from listing station counts to comparing activity at locations under comparable conditions.


2. How does the number of passengers on the train change along the route, and where is occupancy highest?
    Actions: Derive cumulative values, follow changes, and locate maxima
    Targets: Passenger counts along an ordered sequence of stops within each trip
    Abstract Task: Examine how a cumulative quantity changes through a sequence and identify its peak value and position.

I mapped Domain Question 2 to following a sequence because stop order is essential to understanding how the passenger count changes. The target is a derived cumulative quantity, rather than the individual boarding or exiting counts. For an inbound trip, the calculation starts with existing passengers before Cary. For an outbound trip, it starts with passengers boarding at Chicago OTC. Each subsequent count adds boardings and subtracts exits. Locating the maximum answers both how high the count becomes and where that happens. This abstraction helped me distinguish passenger movement at a stop from the number of passengers present between stops.


3. How do passenger volumes differ between express and non-express trains?
    Actions: Group, summarize, and compare
    Targets: Trip-level boarding totals and peak passenger counts grouped by service category
    Abstract Task: Compare the typical values and variation of quantitative measures between two categories.

I mapped Domain Question 3 to comparison between categories because express and non-express are service labels. The phrase "passenger volumes" needs a consistent definition, so I chose total boardings during the observed commute and peak passenger count as two complementary measures. Total boardings describe how many passengers enter the car over the observed segment, while the peak describes its greatest passenger load. Comparing typical values and their variation across trips is more informative than comparing group totals when the groups contain different numbers of observations. Service categories can be assigned from the recorded stop patterns. Comparisons should retain direction and departure-time context because those factors also differ between the observed services. This abstraction made the question more precise and showed that an observed difference cannot establish that express service caused it.


4. How do boarding, exiting, and occupancy patterns vary by weekday and train service?
    Actions: Filter, group, compare, and identify recurring patterns
    Targets: Boarding counts, exiting counts, and derived passenger counts grouped by weekday and service identifier
    Abstract Task: Compare quantitative patterns across combinations of categories and determine whether differences recur across observations.

I mapped Domain Question 4 to comparison across combinations of categories because weekday and train service jointly define the groups of interest. Filtering lets a user focus on a service or direction before comparing weekdays, while examining repeated observations helps distinguish a recurring pattern from one unusual trip. The targets include boarding and exiting counts as well as derived passenger counts because these describe different aspects of activity. This abstraction also exposed a limitation: asthe sampling schedule links certain services to certain weekdays due to the sampling schedule being limited by the nature of my commute, so not every weekday-service combination is available. The visualization can support comparisons among the observed combinations, but cannot isolate an independent weekday effect or establish explanations such as hybrid work schedules.


#### Task 5: Visualization sketches

#### Task 6: Summarizing

#### Task 7: Collaboration process
