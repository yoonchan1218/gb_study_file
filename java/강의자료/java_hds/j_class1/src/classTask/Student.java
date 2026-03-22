package classTask;

public class Student {
	int total;
	double average;
	Subject[] arSubject;
	
	public Student() {;}

	public Student(Subject[] arSubject) {
		this.arSubject = arSubject;
		
		for (int i = 0; i < arSubject.length; i++) {
			total += arSubject[i].score;
		}
		
		average = (double)total / arSubject.length; 
	}
	
}






