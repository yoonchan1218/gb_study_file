package list.task.fruit;

import java.util.ArrayList;
import java.util.List;

import list.task.DBConnecter;

public class Market {
//	- 과일 추가
	public void add(Fruit fruit) {
		DBConnecter.fruits.add(new Fruit(fruit));
	}
	
//	- 과일 삭제
	public void delete(String name) {
		for (int i = 0; i < DBConnecter.fruits.size(); i++) {
			if(DBConnecter.fruits.get(i).getName().equals(name)) {
				DBConnecter.fruits.remove(i);
				break;
			}
		}
	}
	
//	- 과일 가격이 평균 가격보다 낮은 지 검사
	public boolean checkPrice(int price) {
		int total = 0;
		double average = 0.0;

		for (int i = 0; i < DBConnecter.fruits.size(); i++) {
			total += DBConnecter.fruits.get(i).getPrice();
		}
		
		average = (double)total / DBConnecter.fruits.size();
		
		return average > price;
		
	}
	
//	- 과일 전체 조회
	public List<Fruit> findAll(){
		ArrayList<Fruit> fruits = new ArrayList<Fruit>();
		for (int i = 0; i < DBConnecter.fruits.size(); i++) {
			fruits.add(new Fruit(DBConnecter.fruits.get(i)));
		}
		return fruits;
	}
	
//	- 과일 이름으로 가격 조회
	public int findPriceByName(String fruitName) {
		for (int i = 0; i < DBConnecter.fruits.size(); i++) {
			if(DBConnecter.fruits.get(i).getName().equals(fruitName)) {
				return DBConnecter.fruits.get(i).getPrice();
			}
		}
		
		return -1;
	}
}













