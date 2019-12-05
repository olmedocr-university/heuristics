#include <string>
#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>

using namespace std;

class node {
public:
	string type; //stop or school
	string name;
	string schoolName;
	vector<node> adjacent;
	vector<int> cost;
	node(string type, string name, string schoolName, vector<node> adjacent, vector<int> cost) {
		
	}
};
class state {
public:
	node* buspos;
	int capacity;
	int g;
	string initPos;
	vector<node> nodeList;
	vector<vector<string>> studentsInNodes;
	vector<string> students;
	state* parent;
	state(node* buspos, int capacity, int g, string initPos, vector<node> nodeList, vector<vector<string>> studentsInNodes, vector<string> students) {
		this->buspos = buspos;
		this->capacity = capacity;
		this->g = g;
		this->initPos = initPos;
		this->nodeList = nodeList;
		this->studentsInNodes = studentsInNodes;
		this->students = students;
	}
};
int nodePos(string n, vector<node> nodeList) {
	for (int i = 0; i < nodeList.size; i++) {
		if (nodeList[i].name==n) {
			return i;
		}
		return -1;
	}
}
vector<state> successors(state s) {
	vector<state> out;
	//drop off student
	if (s.buspos->type == "school") {
		for (int i = 0; i < s.students.size; i++) {
			if (s.buspos->schoolName == s.students[i]) {
				state newState = state(s.buspos, s.capacity, s.g, s.initPos, s.nodeList, s.studentsInNodes, s.students);
				newState.studentsInNodes[nodePos(newState.buspos->name, newState.nodeList)].push_back(s.students[i]);
				newState.students.erase(newState.students.begin() + i);
				out.push_back(newState);
			}
		}
	}
	//pick up student
	if (s.buspos->type == "stop" && s.students.size < s.capacity) {
		vector<string> temp = s.studentsInNodes[nodePos(s.buspos->name, s.nodeList)];
		for (int i = 0; i < temp.size; i++) {
			state newState = state(s.buspos, s.capacity, s.g, s.initPos, s.nodeList, s.studentsInNodes, s.students);
			newState.students.push_back(temp[i]);
			newState.students.erase(newState.students.begin() + i);
			out.push_back(newState);
		}
	}
	//move
	for (int i = 0; i < s.buspos->adjacent.size;i++) {
		state newState = state(&s.buspos->adjacent[i], s.capacity, s.g + s.buspos->cost[i], s.initPos, s.nodeList, s.studentsInNodes, s.students);
		out.push_back(newState);
	}
	return out;
}
bool goal(state s) {
	if (s.buspos->name!=s.initPos || s.students.size>0) {
		return false;
	}
	for (int i = 0; i < s.nodeList.size; i++) {
		if (s.nodeList[i].type == "stop" && s.studentsInNodes[i].size > 0) {
			return false;
		}
		if (s.nodeList[i].type == "college") {
			for (int k=0; k < s.studentsInNodes[i].size; k++){
				if (s.studentsInNodes[i][k] != s.nodeList[i].schoolName){
					return false;
				}
			}
		}
	}
	return true;
}

bool equalStates(state s1,state s2) {
	if (s1.buspos->name != s2.buspos->name || s1.students.size != s2.students.size || s1.studentsInNodes.size != s2.studentsInNodes.size) {
		return false;
	}
	for (int i = 0; i < s1.students.size; i++) {
		if (s1.students[i]!=s2.students[i]) {
			return false;
		}
	}
	for (int i = 0; i < s1.studentsInNodes.size; i++) {
		if (s1.studentsInNodes[i].size != s2.studentsInNodes[i].size) {
			return false;
		}
		for (int k = 0; k < s1.studentsInNodes[i].size; k++) {
			if (s1.studentsInNodes[i][k] != s2.studentsInNodes[i][k]) {
				return false;
			}
		}
	}
	return true;
}

/*int main(int argc, char* argv[]) {

}*/