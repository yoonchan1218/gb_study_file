package stringTest;

public class StringTask {
	public static void main(String[] args) {
//		아래의 주소에서 "/samsung"만 분리하여 출력한다.
//		www.naver.com/baseball/samsung
//		String url = "www.naver.com/baseball/samsung";
//		int targetIndex = url.lastIndexOf("/");
//		String target = url.substring(targetIndex);
//		
//		System.out.println(target);
		
//		아래의 주소들을 배열에 담고, 마지막 경로가 samsung인 것만 출력한다.
//		www.naver.com/baseball/lg
//		www.naver.com/phone/samsung
//		www.naver.com/baseball/lotte
//		www.naver.com/baseball/kt
//		www.naver.com/baseball/samsung
		
		String[] arData = {
				"www.naver.com/baseball/lg",
				"www.naver.com/phone/samsung",
				"www.naver.com/baseball/lotte",
				"www.naver.com/baseball/kt",
				"www.naver.com/baseball/samsung"
		};
		
		for (int i = 0; i < arData.length; i++) {
			String[] arUrl = arData[i].split("/");
			String target = arUrl[arUrl.length - 1];
			
			if(target.equals("samsung")) {
				System.out.println(arData[i]);
			}
		}
		
	}
}









