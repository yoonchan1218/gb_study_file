package set.test;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.IntStream;

public class SpeedTest {
	public static void main(String[] args) {
		final int SIZE = 10_000_000;
		final List<Integer> ARRAY_LIST = new ArrayList<Integer>(SIZE);
		final Set<Integer> HASH_SET = new HashSet<Integer>(SIZE);
		final int DATA = 6_300_000;
		
		IntStream.range(0, SIZE).forEach(data -> {
			ARRAY_LIST.add(data);
			HASH_SET.add(data);
		});
		
		Instant start = Instant.now();
		ARRAY_LIST.contains(DATA);
		Instant end = Instant.now();
		long elapsedTime = Duration.between(start, end).toMillis();
		System.out.println("arrayList: " + elapsedTime * 0.001 + "초");
		
		start = Instant.now();
		HASH_SET.contains(DATA);
		end = Instant.now();
		elapsedTime = Duration.between(start, end).toMillis();
		System.out.println("hashSet: " + elapsedTime * 0.001 + "초");
		
	}
}
















