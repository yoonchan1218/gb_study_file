package com.example.controller.controller;

import com.example.controller.domain.Member;
import com.example.controller.domain.School;
import com.example.controller.domain.Student;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import org.springframework.web.servlet.view.RedirectView;

import java.util.ArrayList;
import java.util.Arrays;

@Controller
@RequestMapping("/ex/**")
@Slf4j
public class ExampleController {

//    @RequestMapping(value = "ex01", method = RequestMethod.GET, consumes = {}, produces = {})
    @GetMapping("ex01")
    public String ex01(){
        log.info("ex01...................");
        return "ex/ex01";
    }

//    ex02를 선언하고, 본인의 이름을 콘솔창에 출력한다.
//    알맞은 경로에 ex02.html.html을 생성하고 h1태그로 본인 이름을 출력한다.
    @GetMapping("ex02")
    public String ex02(){
        log.info("{}", "한동석");
        return "ex/ex02";
    }

    @GetMapping("ex03")
    public String ex03(int age, Model model){
        log.info("{}..............", age);
        model.addAttribute("age", age);
        return "ex/ex03";
    }

//    ex04를 선언하고,
//    이름을 전달받은 뒤 HTML에서 h1태그로 출력하기
    @GetMapping("ex04")
    public void ex04(@ModelAttribute("name") String name){
        log.info("{}.............", name);
    }

    @GetMapping("ex05")
    public String ex05(Member member, Model model){
        log.info("{}.............", member);
        model.addAttribute("member", member);
        return "ex/ex05";
    }
    
//    학생 객체 생성(이름, 국어, 영어, 수학)
//    Convention에 맞게 제작
//    ex06을 선언하고,
//    학생의 모든 정보 및 총합과 평균 출력
    @GetMapping("ex06")
    public String ex06(Student student, Model model){
        model.addAttribute("student", student);
        return "ex/ex06";
    }

//    @GetMapping("ex07")
//    public String ex07(String[] arData, Model model) {
//        log.info(Arrays.toString(arData));
//        model.addAttribute("arData", arData);
//        return "ex/ex07";
//    }

//    Simple Type: int, String, 배열(String[]), Date, Enum 등
//    @RequestParam을 default로 생각하여 받은 값을 그대로 매핑하여 바인딩함.

//    Complex Type: 사용자 정의 객체(DTO), Map, List 등
//    객체로 생각하여 받은 값을 해당 객체의 필드 내에서 매핑하려고 함.
//    @RequestParam을 붙여주면 받은 값을 개드로 매핑하여 바인딩함.

//    ArrayList일 경우 내부적으로 Converter가 실행되어 알맞은 패턴으로 나누어 담아준다.
//    1. 구분점 패턴: ?names=사과, 딸기
//    2. 중복키 패턴: ?names=사과&names=딸기
    @GetMapping("ex07")
    public String ex07(@RequestParam ArrayList<String> datas, Model model) {
        log.info("{}", datas);
        model.addAttribute("datas", datas);
        return "ex/ex07";
    }

//    ex08.html에서 체크박스 3개 구성
//    완료 버튼 클릭 시, GET 방식으로 다음과 같이 요청한다.
//    /ex/ex09
    @GetMapping("ex08")
    public String ex08(){
        return "ex/ex08";
    }

//    ex09를 선언하고,
//    사용자가 선택한 체크박스 value를 ex09.html에 출력한다.
    @PostMapping("ex09")
    public String ex09(@RequestParam("data") String[] arData, Model model) {
        log.info(Arrays.toString(arData));
        model.addAttribute("arData", arData);
        return "ex/ex09";
    }

    @GetMapping("ex10")
    public String goToEx10() {
        return "ex/ex10";
    }

    @PostMapping("ex10")
    public RedirectView ex10(School school, RedirectAttributes redirectAttributes) {
        log.info(school.toString());
//        다음 컨트롤러에서 사용할 때
//        redirectAttributes.addAttribute("school", school);
//        화면에서 사용할 때
        redirectAttributes.addFlashAttribute("school", school);
        return new RedirectView("/ex/school");
    }

    @GetMapping("school")
    public String school(){
        return "ex/school";
    }

}

















