package classTask;

// 화면
// 학생의 과목 정보를 입력받은 뒤 총점과 평균을 출력한다.
// 학생의 과목 정보는 생성자로 초기화한다.
// 과목 정보는 점수와 과목명이 있으며, 학생 한 명당 여러 과목 정보를 가지고 있다.
// Student.java, Subject.java
public class ClassTask04 {
	public static void main(String[] args) {
		Subject[] arSubject = {
			new Subject("국어", 30),	
			new Subject("영어", 80),	
			new Subject("수학", 100)	
		};
		
		Student 한동석 = new Student(arSubject);
		
		System.out.println(한동석.total);
		System.out.println(한동석.average);
	}
}















