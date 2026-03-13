//Учет финансов позволяет пользователю вести учёт личных доходов и расходов. Программа поддерживает добавление, просмотр, удаление записей, 
// а также расчёт финансовой статистики: общие доходы и расходы, баланс, разбивка по категориям.
// Интерфейс реализован в виде циклического меню с обработкой ошибок ввода.
//
//
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <limits>
#include <ctime>

using namespace std;
struct Operation {
    int id;
    string type;       
    string category;
    double amount;
    string date;        
    string description;
};

vector<Operation> operations;
int nextId = 1;
const string DATA_FILE = "finance_data.txt";

void clearScreen() {
    system("cls"); 
}

bool isValidDate(const string& date) {
    if (date.length() != 10) return false;
    if (date[4] != '-' || date[7] != '-') return false;
    for (int i = 0; i < 10; i++) {
        if (i == 4 || i == 7) continue;
        if (!isdigit(date[i])) return false;
    }
    return true;
}
void addOperation() {
    Operation op;
    op.id = nextId++;

    cout << "Тип (доход/расход): ";
    cin >> op.type;
    cout << "Категория: ";
    cin >> op.category;
    cout << "Сумма: ";
    cin >> op.amount;
    cout << "Дата (YYYY-MM-DD): ";
    cin >> op.date;
    cout << "Описание (можно пропустить, введите -): ";
    cin.ignore();
    getline(cin, op.description);

    if (op.description == "-") op.description = "";

    if (op.type != "доход" && op.type != "расход") {
        cout << "Ошибка: тип должен быть 'доход' или 'расход'.\n";
        return;
    }
    if (op.amount <= 0) {
        cout << "Ошибка: сумма должна быть положительной.\n";
        return;
    }
    if (!isValidDate(op.date)) {
        cout << "Ошибка: неверный формат даты.\n";
        return;
    }

    operations.push_back(op);
    cout << "Запись добавлена.\n";
}

void printOperation(const Operation& op) {
    cout << "ID: " << op.id
        << " Тип: " << op.type
        << " Категория: " << op.category
        << " Сумма: " << fixed << setprecision(2) << op.amount
        << " Дата: " << op.date
        << " Описание: " << (op.description.empty() ? "-" : op.description) << endl;
}

void viewAll() {
    if (operations.empty()) {
        cout << "Нет записей.\n";
        return;
    }
    for (const auto& op : operations) {
        printOperation(op);
    }
}

void viewByType() {
    string type;
    cout << "Введите тип (доход/расход): ";
    cin >> type;
    for (const auto& op : operations) {
        if (op.type == type) {
            printOperation(op);
        }
    }
}

void viewByDateRange() {
    string start, end;
    cout << "Начальная дата (YYYY-MM-DD): ";
    cin >> start;
    cout << "Конечная дата (YYYY-MM-DD): ";
    cin >> end;
    for (const auto& op : operations) {
        if (op.date >= start && op.date <= end) {
            printOperation(op);
        }
    }
}

void deleteOperation() {
    int id;
    cout << "Введите ID записи для удаления: ";
    cin >> id;

    auto it = remove_if(operations.begin(), operations.end(),
        [id](const Operation& op) { return op.id == id; });
    if (it != operations.end()) {
        operations.erase(it, operations.end());
        cout << "Запись удалена.\n";
    }
    else {
        cout << "Запись с таким ID не найдена.\n";
    }
}

void showStats() {
    double totalIncome = 0, totalExpense = 0;
    for (const auto& op : operations) {
        if (op.type == "доход") totalIncome += op.amount;
        else if (op.type == "расход") totalExpense += op.amount;
    }

    cout << "Общий доход: " << totalIncome << endl;
    cout << "Общий расход: " << totalExpense << endl;
    cout << "Баланс: " << totalIncome - totalExpense << endl;

    vector<string> categories;
    vector<double> catIncome, catExpense;

    for (const auto& op : operations) {
        auto it = find(categories.begin(), categories.end(), op.category);
        if (it == categories.end()) {
            categories.push_back(op.category);
            catIncome.push_back(0);
            catExpense.push_back(0);
            it = categories.end() - 1;
        }
        int idx = it - categories.begin();
        if (op.type == "доход") catIncome[idx] += op.amount;
        else catExpense[idx] += op.amount;
    }

    cout << "\nСтатистика по категориям:\n";
    for (size_t i = 0; i < categories.size(); i++) {
        cout << categories[i] << ": доход = " << catIncome[i]
            << ", расход = " << catExpense[i] << endl;
    }
}

void saveToFile() {
    ofstream file(DATA_FILE);
    if (!file) {
        cout << "Ошибка сохранения файла.\n";
        return;
    }
    for (const auto& op : operations) {
        file << op.id << "|" << op.type << "|" << op.category << "|"
            << op.amount << "|" << op.date << "|" << op.description << "\n";
    }
    file.close();
    cout << "Данные сохранены.\n";
}

void loadFromFile() {
    ifstream file(DATA_FILE);
    if (!file) {
        cout << "Файл не найден. Будет создан новый при сохранении.\n";
        return;
    }
    operations.clear();
    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string token;
        Operation op;
        getline(ss, token, '|'); op.id = stoi(token);
        getline(ss, op.type, '|');
        getline(ss, op.category, '|');
        getline(ss, token, '|'); op.amount = stod(token);
        getline(ss, op.date, '|');
        getline(ss, op.description, '|');
        operations.push_back(op);
        if (op.id >= nextId) nextId = op.id + 1;
    }
    file.close();
    cout << "Данные загружены.\n";
}

void showMenu() {
    cout << "\n Учет финансов \n";
    cout << "1. Добавить запись\n";
    cout << "2. Все операции\n";
    cout << "3. По типу\n";
    cout << "4. По дате\n";
    cout << "5. Удалить запись\n";
    cout << "6. Статистика\n";
    cout << "7. Сохранить в файл\n";
    cout << "8. Загрузить из файла\n";
    cout << "0. Выход\n";
    cout << "Выберите действие: ";
}

int main() {
    loadFromFile();

    int choice;
    do {
        showMenu();
        cin >> choice;
        if (cin.fail()) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Неверный ввод. Попробуйте снова.\n";
            continue;
        }

        switch (choice) {
        case 1: addOperation(); break;
        case 2: viewAll(); break;
        case 3: viewByType(); break;
        case 4: viewByDateRange(); break;
        case 5: deleteOperation(); break;
        case 6: showStats(); break;
        case 7: saveToFile(); break;
        case 8: loadFromFile(); break;
        case 0: cout << "Выход.\n"; break;
        default: cout << "Неверный пункт \n";
        }
    } while (choice != 0);

    return 0;
}