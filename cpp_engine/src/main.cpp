#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <ctime>
#include <cctype>
#include <stdexcept>

using namespace std;

// -------------------- User classes --------------------

class User {
private:
    string id;
    string name;
    string email;

public:
    User(string userId, string userName, string userEmail) {
        id = userId;
        name = userName;
        email = userEmail;
    }

    virtual ~User() {
    }

    string getId() const {
        return id;
    }

    string getName() const {
        return name;
    }

    string getEmail() const {
        return email;
    }

    void setName(string newName) {
        if (newName != "") {
            name = newName;
        }
    }

    virtual string role() const = 0;
    virtual string dashboardMessage() const = 0;
};

class Student : public User {
private:
    string course;
    string year;
    string availability;
    string mode;
    vector<string> teaches;
    vector<string> learns;

public:
    Student(string userId, string userName, string userEmail,
            string studentCourse, string studentYear,
            vector<string> skillsToTeach, vector<string> skillsToLearn,
            string studentAvailability, string learningMode)
        : User(userId, userName, userEmail) {
        course = studentCourse;
        year = studentYear;
        teaches = skillsToTeach;
        learns = skillsToLearn;
        availability = studentAvailability;
        mode = learningMode;
    }

    string role() const {
        return "Student";
    }

    string dashboardMessage() const {
        return "Welcome back, " + getName() + ". Ready to exchange a skill?";
    }

    string getCourse() const {
        return course;
    }

    string getYear() const {
        return year;
    }

    string getAvailability() const {
        return availability;
    }

    string getMode() const {
        return mode;
    }

    vector<string> getTeaches() const {
        return teaches;
    }

    vector<string> getLearns() const {
        return learns;
    }

    bool teachesSkill(string skill) const {
        for (int i = 0; i < (int)teaches.size(); i++) {
            if (teaches[i] == skill) {
                return true;
            }
        }
        return false;
    }

    bool wantsSkill(string skill) const {
        for (int i = 0; i < (int)learns.size(); i++) {
            if (learns[i] == skill) {
                return true;
            }
        }
        return false;
    }
};

class Admin : public User {
public:
    Admin(string userId, string userName, string userEmail)
        : User(userId, userName, userEmail) {
    }

    string role() const {
        return "Admin";
    }

    string dashboardMessage() const {
        return "Administrator console: manage the SkillLoop community.";
    }
};

// -------------------- Match class --------------------

class Match {
private:
    string studentId;
    string studentName;
    string sharedSkill;
    double matchScore;
    string explanation;

public:
    Match(string id, string name, string skill, double score, string reason) {
        studentId = id;
        studentName = name;
        sharedSkill = skill;
        matchScore = score;
        explanation = reason;
    }

    double score() const {
        return matchScore;
    }

    string getStudentId() const {
        return studentId;
    }

    string getStudentName() const {
        return studentName;
    }

    string getSharedSkill() const {
        return sharedSkill;
    }

    string getExplanation() const {
        return explanation;
    }

    bool operator>(const Match &other) const {
        return matchScore > other.matchScore;
    }
};

struct Exchange {
    string id;
    string requesterId;
    string targetId;
    string skill;
    string status;
    string createdAt;
};

// -------------------- Helper functions --------------------

string trim(string value) {
    int first = (int)value.find_first_not_of(" \t\r\n");

    if (first == (int)string::npos) {
        return "";
    }

    int last = (int)value.find_last_not_of(" \t\r\n");
    return value.substr(first, last - first + 1);
}

string toLowerCase(string value) {
    for (int i = 0; i < (int)value.length(); i++) {
        value[i] = (char)tolower((unsigned char)value[i]);
    }
    return value;
}

vector<string> splitSkills(string skillText) {
    vector<string> skills;
    stringstream input(skillText);
    string skill;

    while (getline(input, skill, ';')) {
        skill = trim(skill);

        if (skill != "") {
            skills.push_back(skill);
        }
    }

    return skills;
}

string joinSkills(vector<string> skills) {
    string result = "";

    for (int i = 0; i < (int)skills.size(); i++) {
        if (i > 0) {
            result += ";";
        }
        result += skills[i];
    }

    return result;
}

string makeCsvCell(string value) {
    string result = "\"";

    for (int i = 0; i < (int)value.length(); i++) {
        if (value[i] == '"') {
            result += '"';
        }
        result += value[i];
    }

    result += "\"";
    return result;
}

vector<string> readCsvRow(string line) {
    vector<string> values;
    string cell = "";
    bool insideQuotes = false;

    for (int i = 0; i < (int)line.length(); i++) {
        char current = line[i];

        if (current == '"') {
            if (insideQuotes && i + 1 < (int)line.length() && line[i + 1] == '"') {
                cell += '"';
                i++;
            } else {
                insideQuotes = !insideQuotes;
            }
        } else if (current == ',' && !insideQuotes) {
            values.push_back(cell);
            cell = "";
        } else {
            cell += current;
        }
    }

    values.push_back(cell);
    return values;
}

string getCurrentDate() {
    time_t currentTime = time(0);
    tm *date = localtime(&currentTime);

    char dateText[20];
    strftime(dateText, sizeof(dateText), "%Y-%m-%d", date);

    return dateText;
}

// -------------------- DataManager class --------------------

class DataManager {
private:
    string directory;

public:
    DataManager(string folder) {
        directory = folder;
    }

    string getFilePath(string fileName) const {
        return directory + "/" + fileName;
    }

    void initialiseSampleData() {
        ifstream studentCheck(getFilePath("students.csv").c_str());

        if (!studentCheck) {
            ofstream studentFile(getFilePath("students.csv").c_str());

            studentFile << "id,name,email,course,year,teaches,learns,availability,mode\n";
            studentFile << "S001,Aman,aman@example.com,Computer Science,2,Public Speaking;Java,Python;UI Design,Weekday evenings,Online\n";
            studentFile << "S002,Iksha,iksha@example.com,Computer Science,2,Python;UI Design,Java;Public Speaking,Weekday evenings,Online\n";
            studentFile << "S003,Riya,riya@example.com,Information Technology,3,Graphic Design;Python,Java;Graphic Design,Weekends,Hybrid\n";
            studentFile << "S004,Kabir,kabir@example.com,Computer Science,1,Java;Mathematics,Python;Mathematics,Weekday evenings,Online\n";
        }

        ifstream exchangeCheck(getFilePath("exchanges.csv").c_str());

        if (!exchangeCheck) {
            ofstream exchangeFile(getFilePath("exchanges.csv").c_str());
            exchangeFile << "id,requester_id,target_id,skill,status,created_at\n";
        }
    }

    vector<Student> loadStudents() const {
        ifstream file(getFilePath("students.csv").c_str());

        if (!file) {
            throw runtime_error("Cannot open students.csv. Initialise sample data first.");
        }

        vector<Student> students;
        string line;

        getline(file, line); // Skip the heading row.

        while (getline(file, line)) {
            if (trim(line) == "") {
                continue;
            }

            vector<string> row = readCsvRow(line);

            if (row.size() < 9) {
                continue;
            }

            Student student(
                row[0], row[1], row[2], row[3], row[4],
                splitSkills(row[5]), splitSkills(row[6]),
                row[7], row[8]
            );

            students.push_back(student);
        }

        return students;
    }

    void saveStudent(const Student &student) const {
        ofstream file(getFilePath("students.csv").c_str(), ios::app);

        if (!file) {
            throw runtime_error("Cannot write students.csv");
        }

        file << makeCsvCell(student.getId()) << ",";
        file << makeCsvCell(student.getName()) << ",";
        file << makeCsvCell(student.getEmail()) << ",";
        file << makeCsvCell(student.getCourse()) << ",";
        file << makeCsvCell(student.getYear()) << ",";
        file << makeCsvCell(joinSkills(student.getTeaches())) << ",";
        file << makeCsvCell(joinSkills(student.getLearns())) << ",";
        file << makeCsvCell(student.getAvailability()) << ",";
        file << makeCsvCell(student.getMode()) << "\n";
    }

    void updateStudent(const Student &student) const {
        vector<Student> students = loadStudents();
        bool found = false;

        for (int i = 0; i < (int)students.size(); i++) {
            if (students[i].getId() == student.getId()) {
                students[i] = student;
                found = true;
                break;
            }
        }

        if (!found) {
            throw runtime_error("Student not found");
        }

        ofstream file(getFilePath("students.csv").c_str());

        if (!file) {
            throw runtime_error("Cannot rewrite students.csv");
        }

        file << "id,name,email,course,year,teaches,learns,availability,mode\n";

        for (int i = 0; i < (int)students.size(); i++) {
            const Student &current = students[i];

            file << makeCsvCell(current.getId()) << ",";
            file << makeCsvCell(current.getName()) << ",";
            file << makeCsvCell(current.getEmail()) << ",";
            file << makeCsvCell(current.getCourse()) << ",";
            file << makeCsvCell(current.getYear()) << ",";
            file << makeCsvCell(joinSkills(current.getTeaches())) << ",";
            file << makeCsvCell(joinSkills(current.getLearns())) << ",";
            file << makeCsvCell(current.getAvailability()) << ",";
            file << makeCsvCell(current.getMode()) << "\n";
        }
    }

    vector<Exchange> loadExchanges() const {
        vector<Exchange> exchanges;
        ifstream file(getFilePath("exchanges.csv").c_str());

        if (!file) {
            return exchanges;
        }

        string line;
        getline(file, line); // Skip the heading row.

        while (getline(file, line)) {
            if (trim(line) == "") {
                continue;
            }

            vector<string> row = readCsvRow(line);

            if (row.size() >= 6) {
                Exchange exchange;
                exchange.id = row[0];
                exchange.requesterId = row[1];
                exchange.targetId = row[2];
                exchange.skill = row[3];
                exchange.status = row[4];
                exchange.createdAt = row[5];

                exchanges.push_back(exchange);
            }
        }

        return exchanges;
    }

    void saveExchange(const Exchange &exchange) const {
        ofstream file(getFilePath("exchanges.csv").c_str(), ios::app);

        if (!file) {
            throw runtime_error("Cannot write exchanges.csv");
        }

        file << makeCsvCell(exchange.id) << ",";
        file << makeCsvCell(exchange.requesterId) << ",";
        file << makeCsvCell(exchange.targetId) << ",";
        file << makeCsvCell(exchange.skill) << ",";
        file << makeCsvCell(exchange.status) << ",";
        file << makeCsvCell(exchange.createdAt) << "\n";
    }

    void updateExchange(string exchangeId, string newStatus) const {
        vector<Exchange> exchanges = loadExchanges();
        bool found = false;

        for (int i = 0; i < (int)exchanges.size(); i++) {
            if (exchanges[i].id == exchangeId) {
                exchanges[i].status = newStatus;
                found = true;
                break;
            }
        }

        if (!found) {
            throw runtime_error("Exchange not found");
        }

        ofstream file(getFilePath("exchanges.csv").c_str());

        if (!file) {
            throw runtime_error("Cannot rewrite exchanges.csv");
        }

        file << "id,requester_id,target_id,skill,status,created_at\n";

        for (int i = 0; i < (int)exchanges.size(); i++) {
            const Exchange &current = exchanges[i];

            file << makeCsvCell(current.id) << ",";
            file << makeCsvCell(current.requesterId) << ",";
            file << makeCsvCell(current.targetId) << ",";
            file << makeCsvCell(current.skill) << ",";
            file << makeCsvCell(current.status) << ",";
            file << makeCsvCell(current.createdAt) << "\n";
        }
    }
};

// -------------------- Student search --------------------

class StudentService {
private:
    const DataManager &data;

public:
    StudentService(const DataManager &manager) : data(manager) {
    }

    vector<Student> searchStudents(string name) const {
        vector<Student> allStudents = data.loadStudents();
        vector<Student> result;

        for (int i = 0; i < (int)allStudents.size(); i++) {
            if (toLowerCase(allStudents[i].getName()).find(toLowerCase(name)) != string::npos) {
                result.push_back(allStudents[i]);
            }
        }

        return result;
    }

    vector<Student> searchStudents(string name, string course) const {
        vector<Student> nameResults = searchStudents(name);
        vector<Student> result;

        for (int i = 0; i < (int)nameResults.size(); i++) {
            if (toLowerCase(nameResults[i].getCourse()).find(toLowerCase(course)) != string::npos) {
                result.push_back(nameResults[i]);
            }
        }

        return result;
    }

    vector<Student> searchStudents(string name, int year) const {
        vector<Student> nameResults = searchStudents(name);
        vector<Student> result;

        for (int i = 0; i < (int)nameResults.size(); i++) {
            if (nameResults[i].getYear() == to_string(year)) {
                result.push_back(nameResults[i]);
            }
        }

        return result;
    }
};

// -------------------- Matching system --------------------

class MatchEngine {
public:
    double compatibilityScore(const Student &first, const Student &second) const {
        bool firstCanHelp = false;
        bool secondCanHelp = false;

        vector<string> firstSkills = first.getTeaches();
        vector<string> secondSkills = second.getTeaches();

        for (int i = 0; i < (int)firstSkills.size(); i++) {
            if (second.wantsSkill(firstSkills[i])) {
                firstCanHelp = true;
                break;
            }
        }

        for (int i = 0; i < (int)secondSkills.size(); i++) {
            if (first.wantsSkill(secondSkills[i])) {
                secondCanHelp = true;
                break;
            }
        }

        // Both students must be able to teach something the other wants.
        if (!firstCanHelp || !secondCanHelp) {
            return 0;
        }

        double skillScore = 100;
        double availabilityScore = 60;
        double modeScore = 70;

        if (first.getAvailability() == second.getAvailability()) {
            availabilityScore = 100;
        }

        if (first.getMode() == second.getMode()) {
            modeScore = 100;
        }

        double totalScore = (0.70 * skillScore)
                          + (0.20 * availabilityScore)
                          + (0.10 * modeScore);

        return totalScore;
    }

    vector<Match> findMatches(const Student &current, const vector<Student> &allStudents) const {
        vector<Match> matches;

        for (int i = 0; i < (int)allStudents.size(); i++) {
            const Student &other = allStudents[i];

            if (other.getId() == current.getId()) {
                continue;
            }

            string sharedSkill = "";
            vector<string> currentSkills = current.getTeaches();

            for (int j = 0; j < (int)currentSkills.size(); j++) {
                if (other.wantsSkill(currentSkills[j])) {
                    vector<string> otherSkills = other.getTeaches();

                    for (int k = 0; k < (int)otherSkills.size(); k++) {
                        if (current.wantsSkill(otherSkills[k])) {
                            sharedSkill = currentSkills[j] + " ↔ " + otherSkills[k];
                            break;
                        }
                    }
                }

                if (sharedSkill != "") {
                    break;
                }
            }

            if (sharedSkill != "") {
                double score = compatibilityScore(current, other);

                if (score > 0) {
                    Match newMatch(
                        other.getId(),
                        other.getName(),
                        sharedSkill,
                        score,
                        "Reciprocal skill fit; availability and learning mode included."
                    );

                    matches.push_back(newMatch);
                }
            }
        }

        // Put the highest scoring match first.
        for (int i = 0; i < (int)matches.size(); i++) {
            for (int j = i + 1; j < (int)matches.size(); j++) {
                if (matches[j] > matches[i]) {
                    Match temp = matches[i];
                    matches[i] = matches[j];
                    matches[j] = temp;
                }
            }
        }

        return matches;
    }
};

// -------------------- Exchange service --------------------

class ExchangeService {
private:
    const DataManager &data;

public:
    ExchangeService(const DataManager &manager) : data(manager) {
    }

    Exchange create(string requester, string target, string skill) const {
        vector<Exchange> allExchanges = data.loadExchanges();

        Exchange newExchange;
        newExchange.id = "EX" + to_string(1001 + allExchanges.size());
        newExchange.requesterId = requester;
        newExchange.targetId = target;
        newExchange.skill = skill;
        newExchange.status = "Pending";
        newExchange.createdAt = getCurrentDate();

        data.saveExchange(newExchange);
        return newExchange;
    }
};

// -------------------- Program functions --------------------

void printStudent(const Student &student) {
    cout << student.getId() << '\t';
    cout << student.getName() << '\t';
    cout << student.getEmail() << '\t';
    cout << student.getCourse() << '\t';
    cout << student.getYear() << '\t';
    cout << joinSkills(student.getTeaches()) << '\t';
    cout << joinSkills(student.getLearns()) << '\t';
    cout << student.getAvailability() << '\t';
    cout << student.getMode() << '\n';
}

int main(int argc, char *argv[]) {
    try {
        if (argc < 3) {
            cout << "Usage: skillloop_engine COMMAND DATA_DIR [arguments...]\n";
            return 2;
        }

        string command = argv[1];
        string dataFolder = argv[2];

        DataManager data(dataFolder);

        if (command == "init") {
            data.initialiseSampleData();
            cout << "OK\tSample data initialised\n";
        }

        else if (command == "students") {
            vector<Student> allStudents = data.loadStudents();

            for (int i = 0; i < (int)allStudents.size(); i++) {
                printStudent(allStudents[i]);
            }
        }

        else if (command == "add_student" || command == "update_student") {
            if (argc < 12) {
                throw runtime_error("Student details are incomplete.");
            }

            Student student(
                argv[3], argv[4], argv[5], argv[6], argv[7],
                splitSkills(argv[8]), splitSkills(argv[9]),
                argv[10], argv[11]
            );

            if (command == "add_student") {
                data.saveStudent(student);
                cout << "OK\t" << student.getId() << '\n';
            } else {
                data.updateStudent(student);
                cout << "OK\tUpdated\n";
            }
        }

        else if (command == "matches") {
            if (argc < 4) {
                throw runtime_error("Please provide a student ID.");
            }

            vector<Student> allStudents = data.loadStudents();
            bool studentFound = false;
            MatchEngine matchingSystem;

            for (int i = 0; i < (int)allStudents.size(); i++) {
                if (allStudents[i].getId() == argv[3]) {
                    studentFound = true;

                    vector<Match> result = matchingSystem.findMatches(allStudents[i], allStudents);

                    for (int j = 0; j < (int)result.size(); j++) {
                        cout << result[j].getStudentId() << '\t';
                        cout << result[j].getStudentName() << '\t';
                        cout << result[j].getSharedSkill() << '\t';
                        cout << result[j].score() << '\t';
                        cout << result[j].getExplanation() << '\n';
                    }

                    break;
                }
            }

            if (!studentFound) {
                throw runtime_error("Student not found");
            }
        }

        else if (command == "exchanges") {
            vector<Exchange> allExchanges = data.loadExchanges();

            for (int i = 0; i < (int)allExchanges.size(); i++) {
                cout << allExchanges[i].id << '\t';
                cout << allExchanges[i].requesterId << '\t';
                cout << allExchanges[i].targetId << '\t';
                cout << allExchanges[i].skill << '\t';
                cout << allExchanges[i].status << '\t';
                cout << allExchanges[i].createdAt << '\n';
            }
        }

        else if (command == "create_exchange") {
            if (argc < 6) {
                throw runtime_error("Please provide requester ID, target ID and skill.");
            }

            ExchangeService service(data);
            Exchange newExchange = service.create(argv[3], argv[4], argv[5]);

            cout << newExchange.id << '\t' << newExchange.status << '\n';
        }

        else if (command == "update_exchange") {
            if (argc < 5) {
                throw runtime_error("Please provide exchange ID and status.");
            }

            data.updateExchange(argv[3], argv[4]);
            cout << "OK\tUpdated\n";
        }

        else if (command == "user_demo") {
            User *student = new Student(
                "S-DEMO", "Demo Student", "demo@example.com",
                "CS", "1", vector<string>(1, "C++"),
                vector<string>(1, "Python"), "Evenings", "Online"
            );

            User *admin = new Admin("A001", "Demo Admin", "admin@example.com");

            cout << student->role() << '\t' << student->dashboardMessage() << '\n';
            cout << admin->role() << '\t' << admin->dashboardMessage() << '\n';

            delete student;
            delete admin;
        }

        else {
            throw runtime_error("Unknown command: " + command);
        }
    }

    catch (exception &error) {
        cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
