#include <iostream>
#include <string>

using namespace std;

// 1 задание
class Student {
private:
    string name;   
    int age;       
    double grade;  

public:
    Student(string name, int age, double grade) {
        this->name = name;
        this->age = age;
        this->grade = grade;
        cout << "Student constructor called for " << this->name << endl;
    }

    ~Student() {
        cout << "Student destroyed: " << name << endl;
    }

    void setData(string name, int age, double grade) {
        this->name = name;
        this->age = age;
        this->grade = grade;
    }

    void printInfo() {
        cout << "Student Info " << endl;
        cout << "Name: " << name << endl;
        cout << "Age: " << age << endl;
        cout << "Grade: " << grade << endl;
  
    }
};

// задание 2
class Car {
public:
    string brand;  

private:
    int year;      

protected:
    int speed;    

public:
    Car(string brand, int year, int speed) {
        this->brand = brand;
        this->year = year;
        this->speed = speed;
        cout << "Car constructor called for " << this->brand << endl;
    }

    ~Car() {
        cout << "Car destroyed: " << brand << endl;
    }

    void setYear(int y) {
        year = y;
    }

    int getYear() {
        return year;
    }

    void setSpeed(int s) {
        speed = s;
    }

    int getSpeed() {
        return speed;
    }

    void printInfo() {
        cout << " Car Info " << endl;
        cout << "Brand: " << brand << endl;
        cout << "Year: " << year << endl;
        cout << "Speed: " << speed << " km/h" << endl;
    }
};

// 3 задание
class Product {
private:
    string name;  
    double price;  
    int quantity;   

public:
    Product(string name, double price, int quantity) {
        this->name = name;
        this->price = price;
        this->quantity = quantity;
        cout << "Product constructor called for " << this->name << endl;
    }

    ~Product() {
        cout << "Product destroyed: " << name << endl;
    }

    Product* setData(string name, double price, int quantity) {
        this->name = name;
        this->price = price;
        this->quantity = quantity;
        return this;  
    }

    void printInfo() {
        cout << " Product Info " << endl;
        cout << "Name: " << name << endl;
        cout << "Price: $" << price << endl;
        cout << "Quantity in stock: " << quantity << endl;
    }

    void buy(int amount) {
        if (quantity >= amount) {
            quantity -= amount;
            cout << "Purchase successful! " << amount << " " << name
                << "(s) bought." << endl;
        }
        else {
            cout << "Not enough stock! Available: " << quantity
                << ", requested: " << amount << endl;
        }
    }
};

int main() {

    Student s1("Alex", 20, 4.5);
    s1.printInfo();

    Student s2 = s1;
    cout << "\n--- Copy of Student (s2) ---" << endl;
    s2.printInfo();

    cout << "\n Modifying copy (s2) " << endl;
    s2.setData("Bob", 22, 3.8);
    cout << "Original s1:" << endl;
    s1.printInfo();
    cout << "Modified copy s2:" << endl;
    s2.printInfo();

  // 2 задание

    Car c1("Toyota", 2020, 180);
    c1.printInfo();

    cout << "\n Modifying car data " << endl;
    c1.setYear(2021);
    c1.setSpeed(200);
    c1.brand = "Toyota Camry"; 
    c1.printInfo();

    // 3 задание
    Product p1("Laptop", 1500.0, 10);
    p1.printInfo();

    cout << "\n Buying 3 laptops " << endl;
    p1.buy(3);
    p1.printInfo();
    cout << "\n Trying to buy 8 laptops" << endl;
    p1.buy(8);
    p1.printInfo();

    cout << "\n Using setData with this pointer " << endl;
    p1.setData("Gaming Laptop", 2500.0, 5)->printInfo();  

    return 0;
}