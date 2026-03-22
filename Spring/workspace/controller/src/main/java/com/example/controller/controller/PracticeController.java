package com.example.controller.controller;


import com.example.controller.domain.Book;
import com.example.controller.domain.Calc;
import com.example.controller.domain.Order;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.ArrayList;
import java.util.Arrays;


@Controller
@Slf4j
@RequestMapping("/practice/**")
public class PracticeController {

    @GetMapping("hello")
    public String hello(){
        log.info("안녕하세요, Spring!");
        return "practice/hello";
    }

    @GetMapping("info")
    public String info(int age, Model model){
        log.info("{}............",age);
        model.addAttribute("age", age);
        return "practice/info";
    }

    @GetMapping("calculator")
    public String calculator(Calc calc, Model model){
        log.info("{}............",calc);
        model.addAttribute("calc", calc);
        return "practice/calculator";
    }

    @GetMapping("book")
    public String book(Book book, Model model){
        log.info("{}............",book);
        model.addAttribute("book", book);
        return "practice/book";
    }

    @GetMapping("hobby-form")
    public String hobbyForm(){
        log.info("콘솔 들어옴");
        return "practice/hobby-form";
    }

    @PostMapping("hobby-result")
    public String hobbyResult(@RequestParam("hobby") ArrayList<String> hobbys, Model model){
        log.info("{}.......................", hobbys);
        model.addAttribute("hobbys", hobbys);
        return "practice/hobby-result";
    }

    @GetMapping("order-form")
    public String orderForm(){
        return "practice/order-form";
    }

    @PostMapping("order-confirm")
    public String orderConfirm(Order order, Model model){
        log.info("{}......................", order);
        model.addAttribute("order", order);
        return "practice/order-confirm";
    }
}
