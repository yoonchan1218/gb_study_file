package stream.task;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.function.Function;
import java.util.function.IntConsumer;
import java.util.function.Predicate;
import java.util.stream.IntStream;

public class StreamTask {
	
	public int change(int data) {
		return 10 - data;
	}
	
	public static void main(String[] args) {
//		10 ~ 1까지 ArrayList에 담고 출력
//		ArrayList<Integer> datas = new ArrayList<Integer>();
//		IntStream.range(0, 10).forEach((data) -> {
//			datas.add(10 - data);
//		});
//		datas.forEach(System.out::println);
		
//		10 ~ 1까지 ArrayList에 담고 출력(map)
//		ArrayList<Integer> datas = new ArrayList<Integer>();
//		StreamTask streamTask = new StreamTask();
//		Function<Integer, Integer> function = streamTask::change;
		
//		IntStream.range(0, 10).map(function::apply).forEach(datas::add);
//		IntStream.range(0, 10).map(streamTask::change).forEach(datas::add);
//		IntStream.range(0, 10).forEach((data) -> {
//			datas.add(10 - data);
//		});
//		IntStream.range(0, 10).forEach(new IntConsumer() {
//			
//			@Override
//			public void accept(int value) {
//				datas.add(10 - value);
//			}
//		});
//		datas.forEach(System.out::println);
		
//		10 ~ 1까지 ArrayList에 담은 후 짝수만 출력한다.
//		ArrayList<Integer> datas = new ArrayList<Integer>();
//		Predicate<Integer> predicate = (data) -> data % 2 == 0;
//		
//		IntStream.range(0, 10).map((data) -> 10 - data).forEach(datas::add);
//		datas.stream().filter(predicate::test).forEach(System.out::println);
		
//		1 ~ 100까지 중 홀수만 ArrayList에 담고 출력한다.
//		ArrayList<Integer> datas = new ArrayList<Integer>();
//		
//		IntStream.rangeClosed(1, 100).filter((data) -> data % 2 != 0).forEach(datas::add);
//		datas.forEach(System.out::println);
		
//		Apple, Banana, Orange
//		위의 문자열들을 ArrayList에 담고 이름에 'n'이 포함된 과일 이름만 출력한다.
//		ArrayList<String> fruits = new ArrayList<String>(Arrays.asList("Apple", "Banana", "Orange"));
//		fruits.stream().filter((fruit) -> fruit.contains("n")).forEach(System.out::println);
		
//		Product 클래스를 선언한다.
//		- 상품명, 가격, 재고
		Product[] arProduct = {
				new Product("핸드폰", 900_000, 14),
				new Product("게임기", 250_000, 754),
				new Product("칫솔", 3_000, 1523)
		};
//		3개의 상품을 담아 놓는다.
		ArrayList<Product> products = new ArrayList<Product>(Arrays.asList(arProduct));
		
//		1. 가격을 모두 출력한다. 단, 30% 할인된 가격으로 출력한다.
		products.stream().map((product) -> (int)(product.getPrice() * 0.7)).forEach(System.out::println);
		
//		2. 모든 재고를 10으로 변경해서 출력한다.
		products.stream().map(Product::getStock).map((stock) -> 10).forEach(System.out::println);
		
//		3. 해당 상품의 가격과 재고를 곱해 총 가격을 출력한다.
		products.stream().map(Product::getTotal).forEach(System.out::println);
		
	}
}














