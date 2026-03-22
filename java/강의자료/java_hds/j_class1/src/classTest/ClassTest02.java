package classTest;

class Car {
	String brand;
	int price;
	String color;
	
	public Car() {;}
	
	public Car(String brand, int price, String color){
		this.brand = brand;
		this.price = price;
		this.color = color;
	}
	
	public Car(String brand, int price) {
		this.brand = brand;
		this.price = price;
	}
	
	public Car(String brand) {
		this.brand = brand;
	}
	
	void printInfo() {
		System.out.println(brand + ", " + price + ", " + color);
	}
}

public class ClassTest02 {
	public static void main(String[] args) {
		Car mom = new Car("Benz", 10000, "Black");
		Car daddy = new Car("BMW");
		Car myCar = new Car("Morning", 2000);
		
		mom.printInfo();
		daddy.printInfo();
		myCar.printInfo();
	}
}
















