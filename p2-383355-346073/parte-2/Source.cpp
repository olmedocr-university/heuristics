#include <string>
#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <fstream>
#include <algorithm>

using namespace std;

class node {
public:
    string type; //stop or school
    //Name of the node
    string name;
    //Name of the school if the node is a school
    string schoolName;
    //Adjacent nodes
    vector<node> adjacent;
    //Cost of edges to adjacent nodes
    vector<int> cost;

    node(string type, string name, string schoolName, vector<node> adjacent, vector<int> cost) {
        this->type = type;
        this->name = name;
        this->schoolName = schoolName;
        this->adjacent = adjacent;
        this->cost = cost;
    }

    node(string type, string name, string schoolName) {
        this->type = type;
        this->name = name;
        this->schoolName = schoolName;
    }

    node() {}
};

class state {
public:
    //Pointer to the node the bus is on
    node buspos;
    //Capacity of the bus
    int capacity;
    //Cumulative cost
    int g;
    //Name of the initial node
    string initPos;
    //List of nodes
    vector<node> nodeList;
    //List of lists of students at each node
    vector<vector<vector<string>>> studentsInNodes;
    //List of students on the bus
    vector<string> students;
    //Pointer to the parent node
    state *parent = NULL;

    state(node buspos, int capacity, int g, string initPos, vector<node> nodeList,
          vector<vector<vector<string>>> studentsInNodes, vector<string> students) {
        this->buspos = buspos;
        this->capacity = capacity;
        this->g = g;
        this->initPos = initPos;
        this->nodeList = nodeList;
        this->studentsInNodes = studentsInNodes;
        this->students = students;
    }

    state(node buspos, int capacity, int g, string initPos, vector<node> nodeList) {
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

    void printState() {
        cout << "Buspos: " << this->buspos.name << " Capacity: " << this->capacity << " g: " << this->g << " InitPos: "
             << this->initPos << endl;
        if (this->students.size() > 0) {
            for (int i = 0; i < (int) this->students.size(); i++) {
                cout << students[i] << " ";
            }
        } else {
            cout << "empty";
        }
        cout << endl << "Adjacencies: " << endl;
        for (int i = 0; i < (int) this->buspos.adjacent.size(); i++) {
            cout << this->buspos.adjacent[i].type << " " << this->buspos.adjacent[i].schoolName << " "
                 << this->buspos.adjacent[i].name << " " << this->buspos.cost[i];
            cout << endl;
        }
        cout << endl;
    }
};

//Find a node's position in the node list based on name
int nodePos(string n, vector<node> nodeList) {
    for (int i = 0; i < (int) nodeList.size(); i++) {
        if (nodeList[i].name == n) {
            return i;
        }
    }
    return -1;
}

vector<state> successors(state s) {
    //output vector
    vector<state> out;
    //Drop off student
    //Only do this if the node is a school
    if (s.buspos.type == "school") {
        for (int i = 0; i < (int) s.students.size(); i++) {
            //If the student and the school match
            if (s.buspos.schoolName == s.students[i]) {
                //Create the new state
                state newState = state(s.buspos, s.capacity, s.g, s.initPos, s.nodeList, s.studentsInNodes, s.students);
                //Add the student to the school node
                vector<vector<string>> temp = newState.studentsInNodes[nodePos(newState.buspos.name,
                                                                               newState.nodeList)];
                bool inserted = false;
                //Look for the student in studentsInNodes
                for (int k = 0; k < (int) temp.size(); k++) {
                    //If found, increase quantity by 1
                    if (temp[k][1] == s.students[i]) {
                        inserted = true;
                        int num = stoi(temp[k][0]) + 1;
                        newState.studentsInNodes[nodePos(newState.buspos.name, newState.nodeList)][k][0] = to_string(
                                num);
                        break;
                    }
                }
                //If not found, create a new student-quantity pair with quantity = 1
                if (inserted == false) {
                    vector<string> stud{"1", s.students[i]};
                    int nodep = nodePos(newState.buspos.name, newState.nodeList);
                    if (newState.studentsInNodes[nodep].size() > 0) {
                        //Keep the studentsInNodes vector ordered for comparison purposes
                        for (int j = 0; j < (int) newState.studentsInNodes[nodep].size(); j++) {
                            //Find the first smaller or equal value
                            if (newState.studentsInNodes[nodep][j][1] >= stud[1]) {
                                //Insert the new pair right before it
                                newState.studentsInNodes[nodep].insert(newState.studentsInNodes[nodep].begin() + j,
                                                                       stud);
                                break;
                                //If all values are smaller, insert at the end
                            } else if (j == (int) newState.students.size() - 1) {
                                newState.studentsInNodes[nodep].push_back(stud);
                            }
                        }
                        //If the vector doesn't have any elements, just insert the element
                    } else {
                        newState.studentsInNodes[nodep].push_back(stud);
                    }
                }
                //Remove the student from the bus
                newState.students.erase(newState.students.begin() + i);
                newState.parent = &s;
                //Add new state to the output vector
                out.push_back(newState);
            }
        }
    }
    //pick up student
    //Only do this if the bus has enough room
    if ((int) s.students.size() < s.capacity) {
        vector<vector<string>> temp = s.studentsInNodes[nodePos(s.buspos.name, s.nodeList)];
        for (int i = 0; i < (int) temp.size(); i++) {
            //If the node is a stop or the node is a school and the student there does not match
            if (s.buspos.type == "stop" || (s.buspos.type == "school" && s.buspos.schoolName != temp[i][1])) {
                //Create new state
                state newState = state(s.buspos, s.capacity, s.g, s.initPos, s.nodeList, s.studentsInNodes, s.students);
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
                        }
                    }
                    //If the vector doesn't have any elements, just insert the element
                } else {
                    newState.students.push_back(temp[i][1]);
                }
                //Remove the student from the node
                int num = stoi(newState.studentsInNodes[nodePos(newState.buspos.name, newState.nodeList)][i][0]);
                //If there are more than 1 students, reduce quantity by 1
                if (num > 1) {
                    num -= 1;
                    newState.studentsInNodes[nodePos(newState.buspos.name, newState.nodeList)][i][0] = to_string(num);
                    //Else, remove the corresponding student-quantity pair
                } else {
                    newState.studentsInNodes[nodePos(newState.buspos.name, newState.nodeList)].erase(
                            newState.studentsInNodes[nodePos(newState.buspos.name, newState.nodeList)].begin() + i);
                }
                newState.parent = &s;
                //Add new state to the output vector
                out.push_back(newState);
            }
        }
    }
    //move
    for (int i = 0; i < (int) s.buspos.adjacent.size(); i++) {
        //Create a state for each adjacent node. The g variable is updated with the cost to move to said node
        state newState = state(s.nodeList[nodePos(s.buspos.adjacent[i].name, s.nodeList)], s.capacity,
                               s.g + s.buspos.cost[i], s.initPos, s.nodeList, s.studentsInNodes, s.students);
        newState.parent = &s;
        out.push_back(newState);
    }
    return out;
}

//Check if the state is the goal
bool goal(state s) {
    //The bus must be in the initial position with no students inside it
    if (s.buspos.name != s.initPos || s.students.size() > 0) {
        return false;
    }
    for (int i = 0; i < (int) s.nodeList.size(); i++) {
        //Stop nodes must have no students
        if (s.nodeList[i].type == "stop" && s.studentsInNodes[i].size() > 0) {
            return false;
        }
        if (s.nodeList[i].type == "college") {
            for (int k = 0; k < (int) s.studentsInNodes[i].size(); k++) {
                //All students in school nodes must be in the correct school
                if (s.studentsInNodes[i][k][1] != s.nodeList[i].schoolName) {
                    return false;
                }
            }
        }
    }
    return true;
}

//Check if two states are equal
bool equalStates(state s1, state s2) {
    //Check name, number of students in bus and number of nodes
    if (s1.buspos.name != s2.buspos.name || s1.students.size() != s2.students.size() ||
        s1.studentsInNodes.size() != s2.studentsInNodes.size()) {
        return false;
    }
    //Check that the students in the bus are the same
    for (int i = 0; i < (int) s1.students.size(); i++) {
        if (s1.students[i] != s2.students[i]) {
            return false;
        }
    }
    //Check that the students at each node are the same
    for (int i = 0; i < (int) s1.studentsInNodes.size(); i++) {
        if (s1.studentsInNodes[i].size() != s2.studentsInNodes[i].size()) {
            return false;
        }
        for (int k = 0; k < (int) s1.studentsInNodes[i].size(); k++) {
            if (s1.studentsInNodes[i][k][0] != s2.studentsInNodes[i][k][0] ||
                s1.studentsInNodes[i][k][1] != s2.studentsInNodes[i][k][1]) {
                return false;
            }
        }
    }
    return true;
}

int h(state s) {
    return 0;
}

//Function to interpret input file and create the initial state
state parseFile(string file) {
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
        vector<node> nodeList;
        for (int i = 0; i < (int) nodes.size(); i++) {
            //The nodes only have the default type, the name and the default schoolname in this step
            nodeList.push_back(node("stop", nodes[i], ""));
        }
        //Add the schools and schoolnames to the nodes
        for (int i = 0; i < (int) schools.size(); i++) {
            for (int k = 0; k < (int) nodeList.size(); k++) {
                if (schools[i][1] == nodeList[k].name) {
                    nodeList[k].type = "school";
                    nodeList[k].schoolName = schools[i][0];
                    break;
                }
            }
        }

        //Add the cost and adjacencies to the nodes
        for (int i = 0; i < (int) nodeList.size(); i++) {
            vector<int> costv;
            vector<node> adjacent;
            for (int k = 0; k < (int) adj.size(); k++) {
                //If a node has a value in the given matrix, add the number to the cost vector and the node to the adjacency list as a pointer
                if (adj[i][k] != "--") {
                    costv.push_back(stoi(adj[i][k]));
                    adjacent.push_back(nodeList[k]);
                }
            }
            //Set the fields of the node
            nodeList[i].cost = costv;
            nodeList[i].adjacent = adjacent;
        }
        //Obtain the initial buspos for creating the state
        int initPosi = 0;
        for (int i = 0; i < (int) nodeList.size(); i++) {
            if (initPos == nodeList[i].name) {
                initPosi = i;
                break;
            }
        }
        state s = state(nodeList[initPosi], capacity, 0, initPos, nodeList);
        //Create the state. The students vector is empty and the studentsInNodes vector must be added later

        //Create a studentsInNodes vector and fill it with as many empty vectors as nodes are
        vector<vector<vector<string>>> studInNodes;
        for (int i = 0; i < (int) nodeList.size(); i++) {
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

void sortedDescInsert(vector<state> *open, vector<state> desc) {
    for (int i = 0; i < (int) desc.size(); i++) {
        int size = (int) open->size();
        for (int k = 0; k < size; k++) {
            //Find the first smaller or equal value
            state item = (*open)[k];
            if (h(item) + item.g >= h(desc[i]) + desc[i].g) {
                //Insert the descendant
                open->insert(open->begin() + k, desc[i]);
                continue;
                //If all values are smaller, insert at the end
            } else if (k == (int) open->size() - 1) {
                open->push_back(desc[i]);
            }
        }
    }
}

int main(int argc, char *argv[]) {
    state init = parseFile(argv[1]);
    //Check if the file exists
    if (init.capacity < 0) {
        return -1;
    }
    vector<state> openList{init};
    vector<state> closedList;

    while (!openList.empty()) {
        bool isCurrentStateVisited = false;
        state currentState = openList.front();

        for (int i = 0; i < closedList.size(); ++i) {
            if (equalStates(currentState, closedList[i])) {
                openList.erase(openList.begin());
                isCurrentStateVisited = true;
                break;
            }
        }
        if (goal(currentState)) {
            cout << "Solution found" << endl;
            break;
        } else if (!isCurrentStateVisited) {
            cout << "Visiting state: "  << endl;
            currentState.printState();
            sortedDescInsert(&openList, successors(currentState));

            cout << "Deleting current state from openList" << endl;
            openList.erase(openList.begin());

            closedList.push_back(currentState);
        }
    }
}
