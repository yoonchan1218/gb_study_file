package com.app.ex;

import java.io.IOException;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

//아이디, 비밀번호 전달 후
//test, 1234 검사
//성공 시, "test님 환영합니다"
//실패 시, 원래 페이지로 다시 돌아가기(동일한 로그인 화면에서, 로그인 오류 메세지 출력)

public class Ex05 extends HttpServlet {
@Override
protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
   req.getRequestDispatcher("/ex05.jsp").forward(req, resp);
}
@Override
   protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
   String id = req.getParameter("id");
   String password = req.getParameter("password");
   
   resp.sendRedirect(req.getContextPath()+ "/ex05-result?id="+id + "&password="+password);
   
}
}
