package com.app.ex;

import java.io.IOException;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class Ex05Result extends HttpServlet{
@Override
protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
   String id = req.getParameter("id");
   String password = req.getParameter("password");
   
   if(id.equals("test")&&password.equals("1234")) {
      req.setAttribute("id", id);
      req.getRequestDispatcher("/ex05-result.jsp").forward(req, resp);
      
   }else{
	  req.setAttribute("error", "아아디나 비밀번호를 다시 확인하세요"); 
      req.getRequestDispatcher("/ex05.jsp").forward(req, resp);
   }
}
}
