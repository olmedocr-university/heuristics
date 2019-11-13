#
# Lab 01
#
# This finds the optimal solution for maximizing the museum's profit
#

/* set of entrances and museum resources */
set ENTRANCES;
set SECONDARY_ENTRANCES within ENTRANCES;
set MAIN_ENTRANCE within ENTRANCES;
set RESOURCES;
set SECONDARY_RESOURCES within RESOURCES;

/* set of  */
set GALLERIES;
set WEST_GALLERIES within GALLERIES;
set EAST_GALLERIES within GALLERIES;
set SPECIAL_GALLERIES_1 within GALLERIES;
set SPECIAL_GALLERIES_2 within GALLERIES;
set ROBOTS;
set EAST_ONLY_ROBOTS within ROBOTS;
set WEST_ONLY_ROBOTS within ROBOTS;

/* parameters */
param reduction {i in RESOURCES};
param cost {i in RESOURCES};
param daily_cost {i in RESOURCES};
param waiting_time {i in ENTRANCES};

param presentation_time {i in ROBOTS};
param energy_required {i in ROBOTS};
param max_energy {i in ROBOTS};
param number_items {i in GALLERIES};

/* decision variables */
var number {i in RESOURCES, j in ENTRANCES} integer, >= 0;
var is_assigned {i in ROBOTS, j in GALLERIES} binary;

/* objective function */
minimize time: sum{i in ENTRANCES} (waiting_time[i] - sum{j in RESOURCES} reduction[j] * number[j,i]) / 3 + sum{i in ROBOTS} (sum{j in GALLERIES} presentation_time[i] * number_items[j] * is_assigned[i,j]);
/*ad, cg(mal), nq, eij, lm(mal), kb, dc, ho(mal)*/

/* constraints */
/* Total investment must be lower or equal to 1000 */
s.t. total_cost: sum{i in ENTRANCES} sum{j in RESOURCES} (daily_cost[j] * number[j,i]) <= 1000;

/* The main entrance shouldn't cost more than 10% of any secondary entrance */
s.t. cost_ratio {i in SECONDARY_ENTRANCES, k in MAIN_ENTRANCE}: sum{j in RESOURCES} (daily_cost[j] * number[j,k]) <= 1.1 * sum{j in RESOURCES} (daily_cost[j] * number[j,i]);

/* The sum of turnstiles and vending machines in any secondary entrance shall be less than those in the main one */
s.t. secondary_resources_and_entrances {i in SECONDARY_ENTRANCES, k in MAIN_ENTRANCE}: 1 + sum{j in SECONDARY_RESOURCES} (number[j,i]) <=  sum{j in SECONDARY_RESOURCES} number[j,k];

/* The number of turnstiles in the north entrance should be less than those in the west one */
s.t. secondary_turnstiles: number['turnstile','north'] + 1 <= number['turnstile','west'];

/* There should be at least 2 of each resource in the main entrance */
s.t. primary_resources {i in RESOURCES, j in MAIN_ENTRANCE}: number[i,j] >= 2;

/* There should be at least 1 of each resource in the secondary entrances */
s.t. secondary_resources {i in SECONDARY_ENTRANCES, j in RESOURCES}: number[j,i] >= 1;

/* The reduction in the average waiting time in the main entrance should be larger than any of the secondary ones */
s.t. reduction_ratio {i in SECONDARY_ENTRANCES, k in MAIN_ENTRANCE}: sum{j in RESOURCES} (number[j,k] * reduction[j]) >= 1 + sum{j in RESOURCES} (number[j,i] * reduction[j]);


/* It is not allowed to have more than one robot assigned to a unique gallery */
s.t. constraint_1a {j in GALLERIES}: sum{i in ROBOTS} is_assigned[i,j] <= 1;

/* Each gallery must have one robot assigned */
s.t. constraint_1b {j in GALLERIES}: sum{i in ROBOTS} is_assigned[i,j] >= 1;

/* Each robot should be assigned in at least 2 galleries */
s.t. constraint_2a {i in ROBOTS}: sum{j in GALLERIES} is_assigned[i,j] >= 2;

/* Each robot can't be in more than 3 galleries */
s.t. constraint_2b {i in ROBOTS}: sum{j in GALLERIES} is_assigned[i,j] <= 3;

/* Robots 3,5 and 6 cannot be assigned to the west galleries  */
s.t. constraint_3 {i in EAST_ONLY_ROBOTS}: sum{j in WEST_GALLERIES} is_assigned[i,j] <= 0;

/* Robots 2 and 4 cannot be assigned to the east galleries */
s.t. constraint_4 {i in WEST_ONLY_ROBOTS}: sum{j in EAST_GALLERIES} is_assigned[i,j] <= 0;

/* Only robots assigned to A or B can be assigned to galleries C and D */
s.t. constraint_5 {i in ROBOTS}: sum{j in SPECIAL_GALLERIES_1} is_assigned[i,j] >= sum{j in SPECIAL_GALLERIES_2} is_assigned[i,j];

/* Each robot has a maximum energy that cannot be surpassed  */
s.t. constraint_6 {i in ROBOTS}: sum{j in GALLERIES} is_assigned[i,j] * number_items[j] * energy_required[i] <= max_energy[i];

/* Galleries in the west side are larger than the ones in the east and require 10% more time */
s.t. constraint_7 {j in WEST_GALLERIES}: sum{i in WEST_ONLY_ROBOTS} is_assigned[i,j] * number_items[j] * presentation_time[i] >= 1.1 * sum{i in EAST_ONLY_ROBOTS} is_assigned[i,j] * number_items[j] * presentation_time[i];

end;
