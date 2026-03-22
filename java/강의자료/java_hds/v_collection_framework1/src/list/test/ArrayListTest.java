package list.test;

import java.util.ArrayList;
import java.util.Collections;

public class ArrayListTest {
	public static void main(String[] args) {
//		<?>: 제네릭(이름이 없는)
//		객체화 시 타입을 지정하는 기법
//		자료구조를 설계할 때 데이터의 타입을 미리 지정해놓을 수 없기 때문에 임시로 타입을 선언한다.
//		따로 다운 캐스팅할 필요가 없으며, 지정할 타입에 제한을 줄 수 있다.
		
//		Wrapper class: 기본 자료형의 클래스 자료형(Integer, Double, ...)
		ArrayList<Integer> datas = new ArrayList<Integer>();
		datas.add(20);
		datas.add(30);
		datas.add(40);
		datas.add(50);
		datas.add(90);
		datas.add(70);
		datas.add(80);
		datas.add(60);
		datas.add(10);
		
		System.out.println(datas);
		System.out.println(datas.size());
		
		for (int i = 0; i < datas.size(); i++) {
			System.out.println(datas.get(i));
		}
		
//		정렬
		Collections.sort(datas);
		System.out.println(datas);
		
//		가운데를 기준으로 좌우 바꾸기
		Collections.reverse(datas);
		System.out.println(datas);
		
//		요소 랜덤하게 섞기
		Collections.shuffle(datas);
		System.out.println(datas);
		
//		추가(삽입), 30뒤에 60을 삽입한다.
//		int index = datas.indexOf(30);
//		
//		if(index != -1) {
//			datas.add(index + 1, 60);
//		}
//		
//		System.out.println(datas);
			
//		수정, 10을 1로 수정한다.
//		if(datas.contains(10)) {
//			int index = datas.indexOf(10);
//			int previousElement = datas.set(index, 1);
//			System.out.println(previousElement);
//			
//			System.out.println(datas);
//		}
		
//		삭제(인덱스로 삭제), 50을 삭제한다.
//		int index = datas.indexOf(50);
//		
//		if(index != -1) {
//			int removedDate = datas.remove(index);
//			System.out.println(removedDate);
//			
//			System.out.println(datas);
//		}
		
//		삭제(값으로 삭제), 20을 삭제한다.
//		if(datas.remove(Integer.valueOf(20))) {
//			System.out.println(datas);
//		}
		
	}
}






















