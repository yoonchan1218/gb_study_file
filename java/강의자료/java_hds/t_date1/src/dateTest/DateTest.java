package dateTest;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

public class DateTest {
	public static void main(String[] args) {
//		기본으로 알아야할 날짜 타입(Date, Calendar)
//		Date: 기본적으로 날짜 계산을 할 때에 사용되는 클래스이다.
//			  하지만 현재 버전에서는 날짜를 조정하거나 활용할 때 여러 이유로 사용되지 않는다.
		
//		Date date = new Date();
//		System.out.println(date);
		
//		deprecated: 사용하는 것을 권장하지 않는다.
//		System.out.println(date.getDate());
		
//		Calendar cal = Calendar.getInstance();
//		System.out.println(cal);
//		System.out.println(cal.get(Calendar.YEAR));
//		System.out.println(cal.get(Calendar.MONTH));
//		System.out.println(cal.get(Calendar.DATE));
		
		Calendar date = Calendar.getInstance();
		date.set(2035, 11, 4);
		System.out.println(date.getTime());
		
//		원하는 형식의 날짜로 변경(Date를 String으로)
//		화면에 출력하겠다!
//		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy년 MM월 dd일");
//		String format = simpleDateFormat.format(date.getTime());
//		System.out.println(format);
		
//		특정 형식의 문자열을 날짜로 변경(String을 Date로)
//		날짜로 연산을 하겠다!
//		String content = "2025-06-25";
//		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
//		try {
//			Date parsedDate = simpleDateFormat.parse(content);
//			System.out.println(parsedDate);
//		} catch (ParseException e) {
////			System.out.println("형식이 맞지 않습니다.");
//			e.printStackTrace();
//		}
		
	}
}












