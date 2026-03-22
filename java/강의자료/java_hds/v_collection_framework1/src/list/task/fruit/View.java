package list.task.fruit;

import list.task.DBConnecter;

public class View {
	public static void main(String[] args) {
		Market market = new Market();
		
		Fruit fruit = new Fruit();
		fruit.setName("사과");
		fruit.setPrice(3000);
		
		market.add(fruit);
		
		System.out.println(DBConnecter.fruits);
	}
}
