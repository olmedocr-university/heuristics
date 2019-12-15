#include <string>
#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <fstream>
#include <algorithm>
#include <deque>

using namespace std;

class node {
public:
    bool type = false; //stop F or school T
    //Name of the node
    string name;
    //Name of the school if the node is a school
    string schoolName;
    //Adjacent nodes
    vector<int> adjacent;
    //Cost of edges to adjacent nodes
    vector<int> cost;

    node(bool type, string name, string schoolName, vector<int> adjacent, vector<int> cost) {
        this->type = type;
        this->name = name;
        this->schoolName = schoolName;
        this->adjacent = adjacent;
        this->cost = cost;
    }

    node(bool type, string name, string schoolName) {
        this->type = type;
        this->name = name;
        this->schoolName = schoolName;
    }

    node() {}

    ~node(void) {};
};

//Find a node's position in the node list based on name
int nodePos(const string n, const vector<node> *nodeList) {
    for (int i = 0; i < (int) nodeList->size(); i++) {
        if ((*nodeList)[i].name == n) {
            return i;
        }
    }
    return -1;
}

class state {
public:
    //Pointer to the node the bus is on
    int buspos = 0;
    //Capacity of the bus
    int capacity;
    //Cumulative cost
    int g;
    //Name of the initial node
    int initPos = 0;
    //List of nodes
    vector<node> *nodeList = NULL;
    //List of lists of students at each node
    vector<vector<vector<string>>> studentsInNodes;
    //List of students on the bus
    vector<string> students;
    //Pointer to the parent node
    state *parent = NULL;

    state(int buspos, int capacity, int g, int initPos, vector<node> *nodeList,
          vector<vector<vector<string>>> studentsInNodes, vector<string> students) {
        this->buspos = buspos;
        this->capacity = capacity;
        this->g = g;
        this->initPos = initPos;
        this->nodeList = nodeList;
        this->studentsInNodes = studentsInNodes;
        this->students = students;
    }

    state(int buspos, int capacity, int g, int initPos, vector<node> *nodeList) {
        this->buspos = buspos;
        this->capacity = capacity;
        this->g = g;
        this->initPos = initPos;
        this->nodeList = nodeList;
    }

    //Special constructor for handling errors
    state(int i) {
        this->capacity = i;
        this->g = 0;
        this->parent = NULL;
    }

    ~state(void) {};

    string printState() const {
        string out =
                "Buspos: " + (*nodeList)[buspos].name + " Capacity: " + to_string(capacity) + " g: " + to_string(g) +
                " InitPos: " + (*nodeList)[initPos].name + "\n";
        if (students.size() > 0) {
            for (int i = 0; i < (int) students.size(); i++) {
                out += students[i] + " ";
            }
        } else {
            out += "empty";
        }
        out += "\nAdjacencies:\n";
        for (int i = 0; i < (int) (*nodeList)[buspos].adjacent.size(); i++) {
            out += (*nodeList)[(*nodeList)[buspos].adjacent[i]].type + " " +
                   (*nodeList)[(*nodeList)[buspos].adjacent[i]].schoolName + " "
                   + (*nodeList)[(*nodeList)[buspos].adjacent[i]].name + " " + to_string((*nodeList)[buspos].cost[i]) +
                   "\n";
        }
        out += "\nStop contents:\n";
        for (int i = 0; i < (int) this->studentsInNodes.size(); i++) {
            if (this->studentsInNodes[i].size() > 0) {
                for (int k = 0; k < (int) this->studentsInNodes[i].size(); k++) {
                    out += (*nodeList)[i].name + ": " + studentsInNodes[i][k][0] + " " + studentsInNodes[i][k][1];
                }
            } else {
                out += (*nodeList)[i].name + ": " + "empty";
            }
            out += "\n";
        }
        out += "\n";
        return out;
    }
};

vector<state> successors(const state *s) {
    //output vector
    vector<state> out;
    //Drop off student
    //Only do this if the node is a school
    if ((*s->nodeList)[s->buspos].type) {
        for (int i = 0; i < (int) s->students.size(); i++) {
            //If the student and the school match
            if ((*s->nodeList)[s->buspos].schoolName == s->students[i]) {
                //Create the new state
                state newState = state(s->buspos, s->capacity, s->g, s->initPos, s->nodeList, s->studentsInNodes,
                                       s->students);
                //Add the student to the school node
                vector<vector<string>> temp = newState.studentsInNodes[newState.buspos];
                bool inserted = false;
                //Look for the student in studentsInNodes
                for (int k = 0; k < (int) temp.size(); k++) {
                    //If found, increase quantity by 1
                    if (temp[k][1] == s->students[i]) {
                        inserted = true;
                        int num = stoi(temp[k][0]) + 1;
                        newState.studentsInNodes[newState.buspos][k][0] = to_string(num);
                        break;
                    }
                }
                //If not found, create a new student-quantity pair with quantity = 1
                if (inserted == false) {
                    vector<string> stud{"1", s->students[i]};
                    if (newState.studentsInNodes[newState.buspos].size() > 0) {
                        //Keep the studentsInNodes vector ordered for comparison purposes
                        for (int j = 0; j < (int) newState.studentsInNodes[newState.buspos].size(); j++) {
                            //Find the first smaller or equal value
                            if (newState.studentsInNodes[newState.buspos][j][1] >= stud[1]) {
                                //Insert the new pair right before it
                                newState.studentsInNodes[newState.buspos].insert(
                                        newState.studentsInNodes[newState.buspos].begin() + j, stud);
                                break;
                                //If all values are smaller, insert at the end
                            } else if (j == (int) newState.students.size() - 1) {
                                newState.studentsInNodes[newState.buspos].push_back(stud);
                            }
                        }
                        //If the vector doesn't have any elements, just insert the element
                    } else {
                        newState.studentsInNodes[newState.buspos].push_back(stud);
                    }
                }
                //Remove the student from the bus
                newState.students.erase(newState.students.begin() + i);
                //Add new state to the output vector
                out.push_back(newState);
            }
        }
    }
    //pick up student
    //Only do this if the bus has enough room
    if ((int) s->students.size() < s->capacity) {
        vector<vector<string>> temp = s->studentsInNodes[s->buspos];
        for (int i = 0; i < (int) temp.size(); i++) {
            //If the node is a stop or the node is a school and the student there does not match
            if (!(*s->nodeList)[s->buspos].type ||
                ((*s->nodeList)[s->buspos].type && (*s->nodeList)[s->buspos].schoolName != temp[i][1])) {
                //Create new state
                state newState = state(s->buspos, s->capacity, s->g, s->initPos, s->nodeList, s->studentsInNodes,
                                       s->students);
                //Add the student to the bus
                //Keep the students vector ordered for comparison purposes
                if (newState.students.size() > 0) {
                    for (int k = 0; k < (int) newState.students.size(); k++) {
                        //Find the first smaller or equal value
                        if (newState.students[k] >= temp[i][1]) {
                            //Insert the new student right before it
                            newState.students.insert(newState.students.begin() + k, temp[i][1]);
                            break;
                            //If all values are smaller, insert at the end
                        } else if (k == (int) newState.students.size() - 1) {
                            newState.students.push_back(temp[i][1]);
                            break;
                        }
                    }
                    //If the vector doesn't have any elements, just insert the element
                } else {
                    newState.students.push_back(temp[i][1]);
                }
                //Remove the student from the node
                int num = stoi(newState.studentsInNodes[newState.buspos][i][0]);
                //If there are more than 1 students, reduce quantity by 1
                if (num > 1) {
                    num -= 1;
                    newState.studentsInNodes[newState.buspos][i][0] = to_string(num);
                    //Else, remove the corresponding student-quantity pair
                } else {
                    newState.studentsInNodes[newState.buspos].erase(
                            newState.studentsInNodes[newState.buspos].begin() + i);
                }
                //Add new state to the output vector
                out.push_back(newState);
            }
        }
    }
    //move
    for (int i = 0; i < (int) (*s->nodeList)[s->buspos].adjacent.size(); i++) {
        //Create a state for each adjacent node. The g variable is updated with the cost to move to said node
        state newState = state((*s->nodeList)[s->buspos].adjacent[i], s->capacity,
                               s->g + (*s->nodeList)[s->buspos].cost[i], s->initPos, s->nodeList, s->studentsInNodes,
                               s->students);
        out.push_back(newState);
    }
    return out;
}

//Check if the state is the goal
bool goal(const state *s) {
    //The bus must be in the initial position with no students inside it
    if (s->buspos != s->initPos || s->students.size() > 0) {
        return false;
    }
    for (int i = 0; i < (int) (*s->nodeList).size(); i++) {
        //Stop nodes must have no students
        if (!(*s->nodeList)[i].type && s->studentsInNodes[i].size() > 0) {
            return false;
        }
        if ((*s->nodeList)[i].type) {
            for (int k = 0; k < (int) s->studentsInNodes[i].size(); k++) {
                //All students in school nodes must be in the correct school
                if (s->studentsInNodes[i][k][1] != (*s->nodeList)[i].schoolName) {
                    return false;
                }
            }
        }
    }
    return true;
}

//Check if two states are equal
bool equalStates(const state *s1, const state *s2) {
    //Check name, number of students in bus and number of nodes
    if ((*s1->nodeList)[s1->buspos].name != (*s2->nodeList)[s2->buspos].name ||
        s1->students.size() != s2->students.size() ||
        s1->studentsInNodes.size() != s2->studentsInNodes.size()) {
        return false;
    }
    //Check that the students in the bus are the same
    for (int i = 0; i < (int) s1->students.size(); i++) {
        if (s1->students[i] != s2->students[i]) {
            return false;
        }
    }
    //Check that the students at each node are the same
    for (int i = 0; i < (int) s1->studentsInNodes.size(); i++) {
        if (s1->studentsInNodes[i].size() != s2->studentsInNodes[i].size()) {
            return false;
        }
        for (int k = 0; k < (int) s1->studentsInNodes[i].size(); k++) {
            if (s1->studentsInNodes[i][k][0] != s2->studentsInNodes[i][k][0] ||
                s1->studentsInNodes[i][k][1] != s2->studentsInNodes[i][k][1]) {
                return false;
            }
        }
    }
    return true;
}

int h(const state *s) {
    return 0;
}

//Function to interpret input file and create the initial state
state parseFile(const string file, vector<node> *nodeL, string *problem) {
    ifstream input(file);
    //Check if the file exists
    if (input.is_open()) {
        unsigned int i = 0;
        string delimiter = " ";
        vector<string> nodes;
        vector<vector<string>> adj;
        vector<vector<string>> schools;
        vector<vector<vector<string>>> students;
        string initPos;
        int capacity = 0;
        //Read the file line by line
        for (string line; getline(input, line); i++) {
            (*problem) += line + "\n";
            vector<string> l;
            auto start = 0U;
            auto end = line.find(delimiter);
            //Split the line at spaces and store each piece in a vector, ignoring ""
            while (end != string::npos) {
                string piece = line.substr(start, end - start);
                if (piece != "") {
                    l.push_back(piece);
                }
                start = end + delimiter.length();
                end = line.find(delimiter, start);
            }
            string piece = line.substr(start, end - start);
            if (piece != "") {
                l.push_back(piece);
            }
            //The first line contains the node names, they are stored in the nodes vector
            if (i == 0) {
                nodes = l;
                //The following lines of the matrix contain adjacencies. Added to adj vector
            } else if (i > 0 && i <= nodes.size()) {
                //The first element is removed since it's just the name
                l.erase(l.begin());
                adj.push_back(l);
                //The first line after the matrix contains the schools
            } else if (i == nodes.size() + 1) {
                //Iterate through 2 elements at a time, since they are a nodename-schoolname pair
                for (int k = 0; k < (int) l.size(); k += 2) {
                    vector<string> schoolpair;
                    //Remove unneeded characters
                    l[k].erase(remove(l[k].begin(), l[k].end(), ':'), l[k].end());
                    l[k + 1].erase(remove(l[k + 1].begin(), l[k + 1].end(), ';'), l[k + 1].end());
                    //Add the node name and the school name to a vector
                    schoolpair.push_back(l[k]);
                    schoolpair.push_back(l[k + 1]);
                    //Push said vector to the schools vector
                    schools.push_back(schoolpair);
                }
                //The next line contains the studens at each node
            } else if (i == nodes.size() + 2) {
                //For each element in the line
                for (int k = 0; k < (int) l.size();) {
                    //Vector representing a stop, which contains student-quantity pairs
                    vector<vector<string>> stop;
                    //This while iterates until a ; is found in one of the elements, the l.size condition must be kept however
                    while (k < (int) l.size()) {
                        //Student-quantity pair
                        vector<string> stopele;
                        //bool controlling if a ; is found
                        bool endS = false;
                        //Remove : from the first element of each stop
                        l[k].erase(remove(l[k].begin(), l[k].end(), ':'), l[k].end());
                        //If the node name is found in the nodes vector, add it to the stop {{nodename}}
                        if (find(nodes.begin(), nodes.end(), l[k]) != nodes.end()) {
                            stopele.push_back(l[k]);
                            stop.push_back(stopele);
                        } else {
                            //If the element of the line is not in the nodes vector, it must belong to a student-quantity pair
                            //Add the quantity to the stop element
                            stopele.push_back(l[k]);
                            //Remove the , and ; from the second element
                            l[k + 1].erase(remove(l[k + 1].begin(), l[k + 1].end(), ','), l[k + 1].end());
                            //Determine if the second element has a semicolon
                            endS = l[k + 1].find(';') != l[k + 1].npos;
                            l[k + 1].erase(remove(l[k + 1].begin(), l[k + 1].end(), ';'), l[k + 1].end());
                            //Add student to the stop element
                            stopele.push_back(l[k + 1]);
                            //Increase loop counter, as two elements have been used
                            k++;
                            //Add the stop element to the stop
                            stop.push_back(stopele);
                        }
                        //Increase loop counter, as there may be more student-quantity pairs for this node
                        k++;
                        //Break the loop if ; is found, as it marks the end of the students in that node
                        if (endS) {
                            break;
                        }
                    }
                    //Add the stop to the students vector
                    students.push_back(stop);
                }
                //The final line contains the bus's capacity and initial position, they are just directly obtained
            } else if (i == nodes.size() + 3) {
                initPos = l[1];
                capacity = stoi(l[2]);
            }
        }
        //Create the nodeList
        for (int i = 0; i < (int) nodes.size(); i++) {
            //The nodes only have the default type, the name and the default schoolname in this step
            nodeL->push_back(node(false, nodes[i], ""));
        }
        //Add the schools and schoolnames to the nodes
        for (int i = 0; i < (int) schools.size(); i++) {
            for (int k = 0; k < (int) nodeL->size(); k++) {
                if (schools[i][1] == (*nodeL)[k].name) {
                    (*nodeL)[k].type = true;
                    (*nodeL)[k].schoolName = schools[i][0];
                    break;
                }
            }
        }

        //Add the cost and adjacencies to the nodes
        for (int i = 0; i < (int) nodeL->size(); i++) {
            vector<int> costv;
            vector<int> adjacent;
            for (int k = 0; k < (int) adj.size(); k++) {
                //If a node has a value in the given matrix, add the number to the cost vector and the node to the adjacency list as a pointer
                if (adj[i][k] != "--") {
                    costv.push_back(stoi(adj[i][k]));
                    adjacent.push_back(k);
                }
            }
            //Set the fields of the node
            (*nodeL)[i].cost = costv;
            (*nodeL)[i].adjacent = adjacent;
        }
        //Obtain the initial buspos for creating the state
        int initPosi = 0;
        for (int i = 0; i < (int) nodeL->size(); i++) {
            if (initPos == (*nodeL)[i].name) {
                initPosi = i;
                break;
            }
        }
        state s = state(initPosi, capacity, 0, initPosi, nodeL);
        //Create the state. The students vector is empty and the studentsInNodes vector must be added later

        //Create a studentsInNodes vector and fill it with as many empty vectors as nodes are
        vector<vector<vector<string>>> studInNodes;
        for (int i = 0; i < (int) nodeL->size(); i++) {
            vector<vector<string>> temp{};
            studInNodes.push_back(temp);
        }
        //Add the student-quantity pairs to the studInNodes vector
        for (int i = 0; i < (int) students.size(); i++) {
            //Obtain position within studInNodes of the given node
            int pos = nodePos(students[i][0][0], s.nodeList);
            //Ignore the first element (it's the node name) and add the student-quantity pairs
            for (int k = 1; k < (int) students[i].size(); k++) {
                studInNodes[pos].push_back(students[i][k]);
            }
        }
        s.studentsInNodes = studInNodes;
        //Return the finished state
        return s;
    } else {
        //Return an error if the file does not exist
        cerr << "Error: File could not be opened" << endl;
        return state(-1);
    }
    input.close();
}

int findState(const deque<state> *v, const state *s) {
    if (v->size() > 0) {
        for (int i = 0; i < (int) v->size(); i++) {
            if (equalStates(&(*v)[i], s)) {
                return i;
            }
        }
    }
    return -1;
}

int sortedDescInsert(deque<state> *open, const state *desc) {
    //If the vector is empty, just insert
    if (open->size() == 0) {
        open->push_back((*desc));
        return 0;
    }
    //If all values are smaller, insert at the end
    state *temp = &(*open)[open->size() - 1];
    if (h(temp) + temp->g <= h(desc) + desc->g) {
        open->push_back((*desc));
        return open->size() - 1;
    }
    for (int k = 0; k < (int) open->size(); k++) {
        //Find the first greater or equal value
        state *item = &(*open)[k];
        if (h(item) + item->g >= h(desc) + desc->g) {
            //Insert the descendant
            open->insert(open->begin() + k, (*desc));
            return k;
        }
    }
}

string solPath(const state *s, int *steps) {
    if (s->parent == NULL) {
        return (*s->nodeList)[s->buspos].name;
    }
    //Different position means movement
    if ((*s->nodeList)[s->buspos].name != (*s->parent->nodeList)[s->parent->buspos].name) {
        (*steps)++;
        return solPath(s->parent, steps) + "->" + (*s->nodeList)[s->buspos].name;
        //Students being longer in the child means that a student was picked up
    } else if (s->students.size() > s->parent->students.size()) {
        string stud = "";
        if (s->parent->students.size() == 0) {
            stud = s->students.back();
        }
        for (int i = 0; i < (int) s->parent->students.size(); i++) {
            if (s->students[i] != s->parent->students[i]) {
                stud = s->students[i];
                break;
            } else if (i == (int) s->parent->students.size() - 1) {
                stud = s->students.back();
            }
        }
        (*steps)++;
        return solPath(s->parent, steps) + "->" + (*s->nodeList)[s->buspos].name + " (Picked up: " + stud + ")";
        //Students being shorter in the child means a student was dropped off
    } else {
        string stud = "";
        if (s->students.size() == 0) {
            stud = s->parent->students.back();
        }
        for (int i = 0; i < (int) s->students.size(); i++) {
            if (s->students[i] != s->parent->students[i]) {
                stud = s->parent->students[i];
                break;
            } else if (i == (int) s->students.size() - 1) {
                stud = s->parent->students.back();
            }
        }
        (*steps)++;
        return solPath(s->parent, steps) + "->" + (*s->nodeList)[s->buspos].name + " (Dropped off: " + stud + ")";
    }
}

void createSolutionFile(string problemName, string problem, string solution) {
    ofstream outfile(problemName + ".output");
    outfile << problem << endl;
    outfile << solution << endl;
    outfile.close();
}

void createSolutionFile(string problemName, string problem) {
    ofstream outfile(problemName + ".output");
    outfile << problem << endl;
    outfile << "No solution" << endl;
    outfile.close();
}

void createStatsFile(string problemName, double time, int overallCost, int steps, int expansions) {
    ofstream outfile(problemName + ".statistics");
    outfile << "Overall time: " << time / 1000 << " s" << endl;
    outfile << "Overall cost: " << overallCost << endl;
    outfile << "# Steps: " << steps << endl;
    outfile << "# Expansions: " << expansions << endl;
    outfile.close();
}


int main(int argc, char *argv[]) {
    //Take timestamp
    using clk = chrono::high_resolution_clock;
    auto t1 = clk::now();
    int steps = 0;
    int ovCost = 0;

    string problem;
    vector<node> nodeL;
    state init = parseFile(argv[1], &nodeL, &problem);
    //Check if the file exists
    if (init.capacity < 0) {
        return -1;
    }
    //A* implementation
    //Open and closed lists
    deque<state> openList{init};
    deque<state> closedList;
    //Bool keeping track of if the solution has been found
    bool solFound = false;
    //Main A* loop
    while (!openList.empty()) {
        //Pop the first state from the ordered open list
        state currentState = openList.front();
        openList.erase(openList.begin());
        //If it is a goal, halt
        if (goal(&currentState)) {
            cout << "Solution found" << endl;
            solFound = true;
            ovCost = currentState.g;
            createSolutionFile(argv[1], problem, solPath(&currentState, &steps));
            break;
        }

        //Generate successors
        vector<state> suc = successors(&currentState);
        closedList.push_back(currentState);
        //For each successor
        for (int i = 0; i < (int) suc.size(); i++) {
            //Check for duplicates in openList and closedList
            int posO = findState(&openList, &suc[i]);
            int posC = findState(&closedList, &suc[i]);
            if (posO >= 0) {
                //If there is a duplicate in open with a lesser f=g+h, ignore successor
                if (h(&suc[i]) + suc[i].g > openList[posO].g + h(&openList[posO])) {
                    continue;
                }
            } else if (posC >= 0) {
                //If there is a duplicate in closed with a lesser f = g + h, ignore successor
                if (h(&suc[i]) + suc[i].g > closedList[posC].g + h(&closedList[posC])) {
                    continue;
                }
            } else {
                //Otherwise, insert successor in its place within the sorted list
                int pos = sortedDescInsert(&openList, &suc[i]);
                openList[pos].parent = &closedList[closedList.size() - 1];
            }
        }
    }
    //Take the second timestamp. Print execution time in seconds with precision of milliseconds
    auto t2 = clk::now();
    double time = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
    createStatsFile(argv[1], time, ovCost, steps, closedList.size());

    //If a solution does not exist
    if (!solFound) {
        cout << "A solution does not exist" << endl;
        createSolutionFile(argv[1], problem);
    }
}