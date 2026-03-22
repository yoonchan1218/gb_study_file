package stream.test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import stream.task.Animal;
import stream.task.TriFunction;

public class StreamTest {
	
	public static int getDoubleTime(int data) {
		return data * 2;
	}
	
	public static void main(String[] args) {
//		배열을 ArrayList로 변경하는 방법
//		Integer[] arData = {10, 20, 30, 40, 50};
//		ArrayList<Integer> datas = new ArrayList<Integer>(Arrays.asList(arData));
//		System.out.println(datas);
		
//		ArrayList를 배열로 변경하는 방법
//		ArrayList<Integer> datas = new ArrayList<Integer>(Arrays.asList(10, 20, 30, 40, 50));
//		Object[] arData = datas.toArray();
//		
//		for(Object data : arData) {
//			System.out.println(data);
//		}
		
//		IntStream: 정수를 다루는 Stream API
		
//		forEach(): 반복
//		여러 값을 가지고 있는 컬렉션 객체 또는 Stream API에서 forEach 메소드를 사용할 수 있다.
//		forEach() 메소드에는 Consumer 인터페이스 타입에 값(구현체)을 전달해야 한다.
//		Consumer는 함수형 인터페이스이기 때문에 람다식을 사용할 수 있다.
//		컬렉션 객체 또는 Stream 객체 안에 있는 값들이 매개변수에 순서대로 담기고,
//		화살표 뒤에서는 실행하고 싶은 문장을 작성한다.
//		IntStream.range(0, 10).forEach((data) -> {System.out.println(data);});
		
//		10 ~ 100까지 출력
//		IntStream.rangeClosed(10, 100).forEach((data) -> {System.out.println(data);});
//		
//		ArrayList<String> colors = new ArrayList<String>(Arrays.asList("검은색", "빨간색", "녹색"));
//		colors.forEach((color) -> {System.out.println(color);});
		
//		참조형
//		1 ~ 10까지 담고 출력
//		ArrayList<Integer> datas = new ArrayList<Integer>();
//		Consumer<Integer> addConsumer = datas::add;
//		Consumer<Integer> printlnConsumer = System.out::println;
//		
//		IntStream.range(1, 11).forEach(addConsumer::accept);
//		datas.forEach(printlnConsumer::accept);
		
//		map(): 변경
//		1 ~ 10까지 ArrayList에 담고 각 값에 2를 곱하여 출력한다.
//		ArrayList<Integer> datas = new ArrayList<Integer>();
		
//		IntStream.range(1, 11).forEach(datas::add);
//		datas.stream().map((data) -> data * 2).forEach(System.out::println);
//		datas.stream().map(StreamTest::getDoubleTime).forEach(System.out::println);
		
//		filter(): 조건
//		10 ~ 1까지 ArrayList에 담은 후 짝수만 출력한다.
//		ArrayList<Integer> datas = new ArrayList<Integer>();
//		IntStream.range(0, 10).map((data) -> 10 - data).forEach(datas::add);
//		datas.stream().filter((data) -> data % 2 == 0).forEach(System.out::println);
		
//		reduce(): 누적 계산
//		ArrayList<Integer> datas = new ArrayList<Integer>();
//		IntStream.range(0, 10).map((data) -> 10 - data).forEach(datas::add);
////		
//		int result = datas.stream().reduce((total, data) -> total + data).orElse(0);
//		System.out.println(result);

//		Optional 객체 맛보기
//		String data = null;
//		Optional<String> foundData = Optional.ofNullable(data);
//		
//		String result = foundData.orElse("없음");
//		result.length();
		
//		심화
//		User[] arUser = {
//				new User(1, "한동석", 20),
//				new User(2, "정찬호", 12)
//		};
//		
//		ArrayList<User> users = new ArrayList<User>(Arrays.asList(arUser));
		
//		만 나이를 계산한다.
//		users.stream().map((user) -> user.getAge() - 1).forEach(System.out::println);
//		users.stream().map(User::getLowerAge).forEach(System.out::println);
		
//		미성년자만 정보 출력
//		users.stream().filter((user) -> user.getAge() < 20).forEach(System.out::println);
		
//		ArrayList<Integer> datas = new ArrayList<Integer>();
//		IntStream.range(1, 11).forEach(datas::add);
//		
//		Collections.shuffle(datas);
		
//		오름차순
//		datas.stream().sorted().forEach(System.out::println);
		
//		내림차순
//		datas.stream().sorted(Collections.reverseOrder()).forEach(System.out::println);
		
//		collect(): 결과를 다양한 타입으로 리턴한다.
//		ArrayList<Integer> datas = new ArrayList<Integer>();
//		IntStream.range(1, 11).forEach(datas::add);
		
//		List<Integer> results = datas.stream().map((data) -> data * 2).collect(Collectors.toList());
//		System.out.println(results);
		
//		ArrayList<String> datas = new ArrayList<String>(Arrays.asList("바나나", "딸기", "수박"));
//		String result = datas.stream().collect(Collectors.joining(", "));
//		
//		System.out.println(result);
		
		Function<String, Animal> generator1 = Animal::new;
		BiFunction<String, Integer, Animal> generator2 = Animal::new;
		TriFunction<String, Integer, String, Animal> generator3 = Animal::new;

		Animal dog1 = generator1.apply("강아지");
		Animal cat1 = generator1.apply("고양이");
		
		Animal dog2 = generator2.apply("강아지", 3);
		Animal cat2 = generator2.apply("고양이", 5);
		
		Animal dog3 = generator3.apply("강아지", 3, "수컷");
		Animal cat3 = generator3.apply("고양이", 5, "암컷");
		
		
		System.out.println(dog1);
		System.out.println(cat1);
		
		System.out.println(dog2);
		System.out.println(cat2);
		
		System.out.println(dog3);
		System.out.println(cat3);
		
	}
}




















