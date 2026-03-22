package set.test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Iterator;
import java.util.stream.IntStream;

public class SetTest {
	public static void main(String[] args) {
//		HashSet<Color> colorSet = new HashSet<Color>(Arrays.asList(new Color("빨간색"), new Color("검은색")));
//		colorSet.add(new Color("빨간색"));
//		
//		System.out.println(colorSet);
		
//		ArrayList<Integer> datas = new ArrayList<Integer>(Arrays.asList(3, 3, 3, 2, 2, 1, 3, 2));
//		HashSet<Integer> dataSet = new HashSet<Integer>(datas);
//		datas = new ArrayList<Integer>(dataSet);
//		
//		System.out.println(datas);
		
		HashSet<String> bloodType = new HashSet<String>();
		bloodType.add("A");
		bloodType.add("B");
		bloodType.add("O");
		bloodType.add("AB");
		bloodType.add("AB");
		bloodType.add("A");
		bloodType.add("A");
		bloodType.add("A");
		bloodType.add("A");
		
		System.out.println(bloodType.toString());
		
		Iterator<String> iter = bloodType.iterator();
		
		while(iter.hasNext()) {
			System.out.println(iter.next());
		}
		
	}
}













