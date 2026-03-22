package list.task.food;

import java.util.ArrayList;

import list.task.DBConnecter;

public class Restaurant {
//	- 음식 추가
	public void insert(Food food) {
		DBConnecter.foods.add(new Food(food));
	}
	
//	- 음식 이름으로 음식 종류 조회
	public String findTypeByName(String name) {
//		빠른 for문
		for(Food food : DBConnecter.foods) {
			if(food.getName().equals(name)) {
				return food.getType();
			}
		}
		
		return null;
	}
	
	
//	- 사용자가 원하는 종류의 음식 전체 조회
	public ArrayList<Food> findAllByType(String type) {
		ArrayList<Food> foods = new ArrayList<Food>();
		
		for(Food food : DBConnecter.foods) {
			if(food.getType().equals(type)) {
				foods.add(new Food(food));
			}
		}
		
		return foods;
	}
	
//	- 음식 종류 수정 후 가격 10% 상승
	public void setFoodType(Food food) {
		food.setPrice((int)(food.getPrice() * 1.1));
		for (int i = 0; i < DBConnecter.foods.size(); i++) {
			if(DBConnecter.foods.get(i).getName().equals(food.getName())) {
				DBConnecter.foods.set(i, new Food(food));
			}
		}
	}
	
//	- 사용자가 원하는 종류의 음식 개수 조회
	public int selectCount(String type) {
		int count = 0;
		
		for(Food food : DBConnecter.foods) {
			if(food.getType().equals(type)) {
				count++;
			}
		}
		
		return count;
	}
}















